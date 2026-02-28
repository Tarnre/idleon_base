from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from idleonlib.profiles.user_profile import UserProfile
from idleonlib.worlds.world5.hole.schematics import get_schematic_bonus_from_profile

from gaming_monte_carlo.simulation.engine import run_simulation
from gaming_monte_carlo.simulation.metrics import Summary, summarize_results
from gaming_monte_carlo.simulation.rules import Rules
from gaming_monte_carlo.simulation.state import TrialConfig


def _existing_file(path_str: str) -> Path:
    """Argparse helper that validates a path exists."""
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File not found: {path}")
    return path


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file into a dict."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Expected top-level JSON object in {path}")
    return raw


def _apply_config_defaults(parser: argparse.ArgumentParser, config: dict[str, Any]) -> None:
    """Apply config-driven defaults to an argparse parser.

    CLI flags should still override these values.
    """
    defaults: dict[str, Any] = {
        "idleon_config": config.get("idleon_config"),
        "schematic_index": config.get("schematic_index"),
        "snail_level": config.get("snail_level"),
        "initial_k": config.get("initial_k"),
        "attempt_energy": config.get("attempt_energy"),
        "trials": config.get("trials"),
        "non_strict": config.get("non_strict"),
    }
    parser.set_defaults(**{k: v for k, v in defaults.items() if v is not None})


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog="gaming-monte-carlo",
        description="Run Monte Carlo simulations using Idleon profile inputs.",
    )

    parser.add_argument(
        "--mc-config",
        type=_existing_file,
        default=None,
        help=(
            "Path to a Monte Carlo config JSON file. Values in this file set "
            "defaults, and any explicit CLI flags override them."
        ),
    )

    parser.add_argument(
        "--idleon-config",
        type=_existing_file,
        default=None,
        help=(
            "Path to Idleon Toolbox-style config.json (or compatible export) "
            "parsed by idleonlib. If omitted, hole bonus defaults to 0."
        ),
    )
    parser.add_argument(
        "--schematic-index",
        type=int,
        default=53,
        help="Hole schematic index used to compute the bonus (default: 53).",
    )

    parser.add_argument("--snail-level", type=int, required=True, help="Snail level.")
    parser.add_argument(
        "--initial-k",
        type=int,
        default=1,
        help="Starting encouragement value (k) for the run.",
    )

    parser.add_argument(
        "--attempt-energy",
        type=int,
        default=5,
        help="Energy cost per attempt.",
    )

    parser.add_argument("--trials", type=int, default=50_000, help="Number of trials to run.")
    parser.add_argument(
        "--non-strict",
        action="store_true",
        help="Allow missing/invalid profile sections to degrade to defaults.",
    )
    return parser


def _parse_args_with_config(argv: list[str] | None) -> argparse.Namespace:
    """Parse CLI args, supporting a JSON config file for defaults."""
    parser = build_parser()

    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--mc-config", type=_existing_file, default=None)
    known, _ = pre.parse_known_args(argv)

    if known.mc_config is not None:
        cfg = _read_json(Path(known.mc_config))
        _apply_config_defaults(parser, cfg)

        if cfg.get("snail_level") is not None:
            for action in parser._actions:  # noqa: SLF001
                if getattr(action, "dest", None) == "snail_level":
                    action.required = False
                    break
        if cfg.get("trials") is not None:
            for action in parser._actions:
                if getattr(action, "dest", None) == "trials":
                    action.required = False

    args = parser.parse_args(argv)
    if args.snail_level is None:
        parser.error("--snail-level is required (or set snail_level in --mc-config)")
    return args


def _hole_bonus_from_args(args: argparse.Namespace) -> float:
    """Compute hole bonus from Idleon config (if provided)."""
    if args.idleon_config is None:
        return 0.0

    profile = UserProfile.from_config_json(Path(args.idleon_config), strict=not args.non_strict)
    return float(get_schematic_bonus_from_profile(t=int(args.schematic_index), profile=profile))


def _simulate_for_k(
    *,
    base_config: TrialConfig,
    rules: Rules,
    n_trials: int,
    k: int,
) -> Summary:
    """Run one simulation with the given k and return its summary."""
    config = TrialConfig(
        snail_level=int(base_config.snail_level),
        initial_k=int(k),
        hole_bonus=float(base_config.hole_bonus),
    )
    results = run_simulation(config=config, rules=rules, n_trials=int(n_trials))
    return summarize_results(results, config=config, rules=rules)


def _auto_find_k_first_decrease(
    *,
    base_config: TrialConfig,
    rules: Rules,
    n_trials: int,
    start_k: int,
) -> tuple[int, dict[int, Summary]]:
    """Increase k until expected energy per success first decreases.

    We evaluate k = start_k, start_k+1, ... until
    expected_energy_per_success decreases relative to the previous k.

    Then we compute summaries for (k-1, k, k+1) and pick the k in that
    bracket with the lowest expected_energy_per_success.

    Returns:
        (best_k, summaries_by_k)
    """
    summaries: dict[int, Summary] = {}

    k0 = max(1, int(start_k))
    for k in range(k0, 20):  # practical guard; bracket is local anyway
        s = _simulate_for_k(base_config=base_config, rules=rules, n_trials=n_trials, k=k)
        summaries[k] = s
        

    best_k = min(summaries, key=lambda kk: summaries[kk].expected_energy_per_success)
    return best_k, summaries


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint."""
    args = _parse_args_with_config(argv)

    hole_bonus = _hole_bonus_from_args(args)

    base_config = TrialConfig(
        snail_level=int(args.snail_level),
        initial_k=int(args.initial_k),
        hole_bonus=hole_bonus,
    )

    rules = Rules(attempt_energy_cost=int(args.attempt_energy))

    best_k, summaries = _auto_find_k_first_decrease(
        base_config=base_config,
        rules=rules,
        n_trials=int(args.trials),
        start_k=int(args.initial_k),
    )

    ks = [k for k in (best_k - 1, best_k, best_k + 1) if k >= 1]

    print("=== k bracket (best_k +/- 1) ===")
    for k in summaries.keys():
        try:
            s = summaries[k]
            print(
                f"k={k:3d} | expected_energy_per_success={s.expected_energy_per_success:.3f}"
            )
        except:
            break

    best_summary = summaries[best_k]
    print("")
    print("=== lowest expected energy ===")
    print(f"best_k={best_k} | expected_energy_per_success={best_summary.expected_energy_per_success:.3f}")
    print("")
    print(best_summary)


if __name__ == "__main__":
    main()
