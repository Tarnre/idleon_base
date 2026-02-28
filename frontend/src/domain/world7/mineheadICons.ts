export const MINEHEAD_UPGRADE_ICON: Record<number, string> = {
  // idx -> URL under public/
  // 0: "/assets/defaultpak/72x72/png_01234_72x72.png",
};

export function mineheadUpgradeIconUrl(upgradeIdx: number): string | null {
  return MINEHEAD_UPGRADE_ICON[upgradeIdx] ?? null;
}