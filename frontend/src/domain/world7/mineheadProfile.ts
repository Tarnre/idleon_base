import type { ResearchBlob } from "./research";
import {
  mineheadUpgradeName,
  MINEHEAD_UPGRADE_INDICES,
} from "./mineheadUpgrades";

export type MineheadCore = {
  opponentIndex: number;
  unk01: number;
  unk02: number;
  unk03: number;
  bonusUnlockLevel: number;
  currency: number;
  unk06: number;
  unk07: number;
  unk08: number;
  unk09: number;
  unk10: number;
  unk11: number;
  unk12: number;
  unk13: number;
  unk14: number;
  unk15: number;
  unk16: number;
  unk17: number;
  unk18: number;
  unk19: number;
  raw: unknown[];
};

export type MineheadUpgrades = {
  /** Always length 50, padded/truncated. */
  byIndex: number[];
  /**
   * Semantic upgrade names from MineheadUPG mapping.
   * Only includes indices we have names for (currently 0..29).
   */
  byName: Record<string, number>;
  raw: unknown[];
};

export type MineheadProfile = {
  core: MineheadCore;
  upgrades: MineheadUpgrades;
};

export function parseMineheadFromResearch(blob: ResearchBlob): MineheadProfile {
  const coreRaw = (blob[7] ?? []) as unknown[];
  const upgRaw = (blob[8] ?? []) as unknown[];

  const core = parseMineheadCore(coreRaw);
  const upgrades = parseMineheadUpgrades(upgRaw);

  return { core, upgrades };
}

export function mineheadUpgradeLevel(
  upgrades: MineheadUpgrades,
  index: number,
): number {
  if (index < 0 || index >= upgrades.byIndex.length) return 0;
  return upgrades.byIndex[index] ?? 0;
}

function toInt(v: unknown): number {
  const n = typeof v === "number" ? v : Number(v);
  return Number.isFinite(n) ? Math.trunc(n) : 0;
}

function toFloat(v: unknown): number {
  const n = typeof v === "number" ? v : Number(v);
  return Number.isFinite(n) ? n : 0;
}

function parseMineheadCore(values: unknown[]): MineheadCore {
  const v = values.slice(0, 20);
  while (v.length < 20) v.push(0);

  return {
    opponentIndex: toInt(v[0]),
    unk01: toFloat(v[1]),
    unk02: toFloat(v[2]),
    unk03: toFloat(v[3]),
    bonusUnlockLevel: toInt(v[4]),
    currency: toFloat(v[5]),
    unk06: toFloat(v[6]),
    unk07: toFloat(v[7]),
    unk08: toFloat(v[8]),
    unk09: toFloat(v[9]),
    unk10: toFloat(v[10]),
    unk11: toFloat(v[11]),
    unk12: toFloat(v[12]),
    unk13: toFloat(v[13]),
    unk14: toFloat(v[14]),
    unk15: toFloat(v[15]),
    unk16: toFloat(v[16]),
    unk17: toFloat(v[17]),
    unk18: toFloat(v[18]),
    unk19: toFloat(v[19]),
    raw: values,
  };
}

function parseMineheadUpgrades(values: unknown[]): MineheadUpgrades {
  const byIndex = values.slice(0, 50).map(toInt);
  while (byIndex.length < 50) byIndex.push(0);

  const byName: Record<string, number> = {};
  for (const idx of MINEHEAD_UPGRADE_INDICES) {
    const name = mineheadUpgradeName(idx);
    byName[name] = byIndex[idx] ?? 0;
  }

  return {
    byIndex,
    byName,
    raw: values,
  };
}