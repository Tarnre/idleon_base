import { MINEHEAD_UPGRADE_NAMES, MINEHEAD_UPGRADE_INDICES } from "./mineheadUpgrades";

export type MineheadUpgradeMeta = {
  /** Same as the key in MINEHEAD_UPGRADE_NAMES (e.g. "numbahs") */
  key: string;

  /** Human-facing label shown in the UI. */
  displayName: string;

  /** If known from MineheadUPG, otherwise null. */
  maxLevel: number | null;

  /** If known from MineheadUPG, otherwise null. */
  multiplier: number | null;

  /** Optional: any extra columns you want later (cost scale, desc, etc.) */
  notes?: string;
};

/**
 * TODO: Populate maxLevel/multiplier/notes from MineheadUPG in idleon1.05_2.
 *
 * This is intentionally safe-by-default: missing values render as "—".
 */
export const MINEHEAD_UPGRADE_META: Record<number, MineheadUpgradeMeta> = Object.fromEntries(
  MINEHEAD_UPGRADE_INDICES.map((idx) => {
    const key = MINEHEAD_UPGRADE_NAMES[idx] ?? `upg_${String(idx).padStart(2, "0")}`;
    return [
      idx,
      {
        key,
        displayName: toTitle(key),
        maxLevel: null,
        multiplier: null,
      } satisfies MineheadUpgradeMeta,
    ];
  }),
) as Record<number, MineheadUpgradeMeta>;

function toTitle(key: string): string {
  return key
    .split("_")
    .map((w) => (w.length ? w[0].toUpperCase() + w.slice(1) : w))
    .join(" ");
}