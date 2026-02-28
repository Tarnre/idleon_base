from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


@dataclass(frozen=True, slots=True)
class MineheadCore:
    """World 7: Minehead core state (Research[7]).

    This is a *named-field* wrapper around the 20-element Minehead core list.

    We only have high-confidence names for a few slots today. The rest are
    kept as stable placeholders (unk_XX) so you never have to remember
    indices during debugging. As we learn semantics from the decompile, we
    can rename fields without changing underlying storage.

    Attributes:
        opponent_index: Best-effort from slot 0.
        unk_01..unk_03: Unknown slots.
        bonus_unlock_level: Best-effort from slot 4.
        currency: Best-effort from slot 5.
        unk_06..unk_19: Unknown slots.
        raw: The original list (length 20) for debugging/round-trip.
    """

    opponent_index: int
    unk_01: float
    unk_02: float
    unk_03: float
    bonus_unlock_level: int
    currency: float
    unk_06: float
    unk_07: float
    unk_08: float
    unk_09: float
    unk_10: float
    unk_11: float
    unk_12: float
    unk_13: float
    unk_14: float
    unk_15: float
    unk_16: float
    unk_17: float
    unk_18: float
    unk_19: float

    raw: tuple[Any, ...]

    @classmethod
    def from_list(cls, values: list[Any]) -> MineheadCore:
        """Parse Minehead core from a raw list.

        Args:
            values: Expected length 20 list from Research[7].

        Returns:
            Parsed MineheadCore with stable named fields.
        """
        v = list(values)
        if len(v) < 20:
            v.extend([0] * (20 - len(v)))
        if len(v) > 20:
            v = v[:20]

        return cls(
            opponent_index=_as_int(v[0]),
            unk_01=_as_float(v[1]),
            unk_02=_as_float(v[2]),
            unk_03=_as_float(v[3]),
            bonus_unlock_level=_as_int(v[4]),
            currency=_as_float(v[5]),
            unk_06=_as_float(v[6]),
            unk_07=_as_float(v[7]),
            unk_08=_as_float(v[8]),
            unk_09=_as_float(v[9]),
            unk_10=_as_float(v[10]),
            unk_11=_as_float(v[11]),
            unk_12=_as_float(v[12]),
            unk_13=_as_float(v[13]),
            unk_14=_as_float(v[14]),
            unk_15=_as_float(v[15]),
            unk_16=_as_float(v[16]),
            unk_17=_as_float(v[17]),
            unk_18=_as_float(v[18]),
            unk_19=_as_float(v[19]),
            raw=tuple(values),
        )

# Index -> semantic name, derived from MineheadUPG() in idleon1.05_2.
MINEHEAD_UPGRADE_NAMES: dict[int, str] = {
    0: "base_damage_i",
    1: "numbahs",
    2: "grid_expansion",
    3: "bettah_numbahs",
    4: "mega_damage_i",
    5: "miney_farmey_i",
    6: "extra_lives",
    7: "base_damage_ii",
    8: "golden_tiles",
    9: "big_hit_combos",
    10: "boom_blocker",
    11: "final_round_fury",
    12: "multiplier_madness",
    13: "moar_moar_multis",
    14: "triple_crown_hunter",
    15: "crown_craze",
    16: "legal_cheating_button",
    17: "awesome_additives",
    18: "always_adding",
    19: "clutch_overtime_block",
    20: "classic_flags",
    21: "mega_damage_ii",
    22: "miney_farmey_ii",
    23: "jackpot_time",
    24: "record_breaking_jackpots",
    25: "base_damage_iii",
    26: "el_cheapo_upgrado",
    27: "mega_damage_iii",
    28: "miney_damagey_synergy",
    29: "rift_guys_upgrade",
}


@dataclass(frozen=True, slots=True)
class MineheadUpgrades:
    """World 7: Minehead upgrade levels (Research[8]).

    Storage is stable as upg_00..upg_49. For debugging/readability,
    semantic upgrade properties are provided for indices that exist in the
    MineheadUPG() table (currently 0..29).

    Attributes:
        upg_00..upg_49: Raw upgrade levels.
        raw: The original list for debugging/round-trip.
    """

    upg_00: int
    upg_01: int
    upg_02: int
    upg_03: int
    upg_04: int
    upg_05: int
    upg_06: int
    upg_07: int
    upg_08: int
    upg_09: int
    upg_10: int
    upg_11: int
    upg_12: int
    upg_13: int
    upg_14: int
    upg_15: int
    upg_16: int
    upg_17: int
    upg_18: int
    upg_19: int
    upg_20: int
    upg_21: int
    upg_22: int
    upg_23: int
    upg_24: int
    upg_25: int
    upg_26: int
    upg_27: int
    upg_28: int
    upg_29: int
    upg_30: int
    upg_31: int
    upg_32: int
    upg_33: int
    upg_34: int
    upg_35: int
    upg_36: int
    upg_37: int
    upg_38: int
    upg_39: int
    upg_40: int
    upg_41: int
    upg_42: int
    upg_43: int
    upg_44: int
    upg_45: int
    upg_46: int
    upg_47: int
    upg_48: int
    upg_49: int

    raw: tuple[Any, ...]

    @classmethod
    def from_list(cls, values: list[Any]) -> MineheadUpgrades:
        """Parse Minehead upgrades from a raw list.

        Args:
            values: Expected length 50 list from Research[8].

        Returns:
            Parsed MineheadUpgrades with stable named fields.
        """
        v = list(values)
        if len(v) < 50:
            v.extend([0] * (50 - len(v)))
        if len(v) > 50:
            v = v[:50]

        as_int = [_as_int(x) for x in v]
        return cls(*as_int, raw=tuple(values))  # type: ignore[arg-type]

    def level(self, index: int) -> int:
        """Return a level by numeric index.

        Args:
            index: Upgrade index.

        Returns:
            Upgrade level, or 0 if out of range.
        """
        if index < 0 or index >= 50:
            return 0
        return getattr(self, f"upg_{index:02d}")

    def upgrade_qty(self, index: int) -> float:
        """Return UpgradeQTY for formulas.

        For now this returns the raw level as a quantity. Later we can
        multiply by MineheadUPG multipliers without changing callers.

        Args:
            index: Upgrade index.

        Returns:
            Quantity as float.
        """
        return float(self.level(index))

    def upgrade_name(self, index: int) -> str:
        """Return the semantic name for an upgrade index, if known."""
        return MINEHEAD_UPGRADE_NAMES.get(index, f"upg_{index:02d}")

    # --- Semantic properties derived from MineheadUPG() ---

    @property
    def base_damage_i(self) -> int:
        return self.upg_00

    @property
    def numbahs(self) -> int:
        return self.upg_01

    @property
    def grid_expansion(self) -> int:
        return self.upg_02

    @property
    def bettah_numbahs(self) -> int:
        return self.upg_03

    @property
    def mega_damage_i(self) -> int:
        return self.upg_04

    @property
    def miney_farmey_i(self) -> int:
        return self.upg_05

    @property
    def extra_lives(self) -> int:
        return self.upg_06

    @property
    def base_damage_ii(self) -> int:
        return self.upg_07

    @property
    def golden_tiles(self) -> int:
        return self.upg_08

    @property
    def big_hit_combos(self) -> int:
        return self.upg_09

    @property
    def boom_blocker(self) -> int:
        return self.upg_10

    @property
    def final_round_fury(self) -> int:
        return self.upg_11

    @property
    def multiplier_madness(self) -> int:
        return self.upg_12

    @property
    def moar_moar_multis(self) -> int:
        return self.upg_13

    @property
    def triple_crown_hunter(self) -> int:
        return self.upg_14

    @property
    def crown_craze(self) -> int:
        return self.upg_15

    @property
    def legal_cheating_button(self) -> int:
        return self.upg_16

    @property
    def awesome_additives(self) -> int:
        return self.upg_17

    @property
    def always_adding(self) -> int:
        return self.upg_18

    @property
    def clutch_overtime_block(self) -> int:
        return self.upg_19

    @property
    def classic_flags(self) -> int:
        return self.upg_20

    @property
    def mega_damage_ii(self) -> int:
        return self.upg_21

    @property
    def miney_farmey_ii(self) -> int:
        return self.upg_22

    @property
    def jackpot_time(self) -> int:
        return self.upg_23

    @property
    def record_breaking_jackpots(self) -> int:
        return self.upg_24

    @property
    def base_damage_iii(self) -> int:
        return self.upg_25

    @property
    def el_cheapo_upgrado(self) -> int:
        return self.upg_26

    @property
    def mega_damage_iii(self) -> int:
        return self.upg_27

    @property
    def miney_damagey_synergy(self) -> int:
        return self.upg_28

    @property
    def rift_guys_upgrade(self) -> int:
        return self.upg_29
    

@dataclass(frozen=True, slots=True)
class MineheadProfileData:
    """World 7: Minehead profile data.

    This is the fully normalized Minehead state extracted from
    Research[7] (core) and Research[8] (upgrades).

    Attributes:
        core: Parsed MineheadCore (named fields instead of raw indices).
        upgrades: Parsed MineheadUpgrades (named upgrade fields).
    """

    core: MineheadCore
    upgrades: MineheadUpgrades

    @property
    def opponent_index(self) -> int:
        """Convenience passthrough for current opponent index."""
        return self.core.opponent_index

    def upgrade_level(self, index: int) -> int:
        """Return upgrade level by numeric index.

        This keeps compatibility with decompile-style references.

        Args:
            index: Upgrade index.

        Returns:
            Upgrade level.
        """
        return self.upgrades.level(index)

    def upgrade_qty(self, index: int) -> float:
        """Return UpgradeQTY for formulas.

        Currently equal to raw level. Later this can apply
        multipliers from MineheadUPG metadata without changing callers.
        """
        return self.upgrades.upgrade_qty(index)