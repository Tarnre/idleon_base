export const MINEHEAD_UPGRADE_NAMES: Record<number, string> = {
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
};

export const MINEHEAD_UPGRADE_INDICES: number[] = Object.keys(MINEHEAD_UPGRADE_NAMES)
  .map((k) => Number(k))
  .sort((a, b) => a - b);

export function mineheadUpgradeName(index: number): string {
  return MINEHEAD_UPGRADE_NAMES[index] ?? `upg_${String(index).padStart(2, "0")}`;
}