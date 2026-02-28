import { useMemo, useState } from "react";
import type { MineheadUpgrades } from "../../domain/world7/mineheadProfile";
import { MINEHEAD_UPGRADE_INDICES, mineheadUpgradeName } from "../../domain/world7/mineheadUpgrades";
import { MINEHEAD_UPGRADE_META } from "../../domain/world7/mineheadUpgradeMeta";
import { mineheadUpgradeIconUrl } from "@/domain/world7/mineheadIcons"

type Props = {
  upgrades: MineheadUpgrades;
};
const iconUrl = mineheadUpgradeIconUrl(selectedIndex);

export default function UpgradeDetails({ upgrades }: Props) {
  const [selectedIndex, setSelectedIndex] = useState<number>(
    MINEHEAD_UPGRADE_INDICES[0] ?? 0
  );

  const level = upgrades.byIndex[selectedIndex] ?? 0;

  const meta = useMemo(() => {
    return (
      MINEHEAD_UPGRADE_META[selectedIndex] ?? {
        key: mineheadUpgradeName(selectedIndex),
        displayName: mineheadUpgradeName(selectedIndex),
        maxLevel: null,
        multiplier: null,
      }
    );
  }, [selectedIndex]);

  const iconUrl = mineheadUpgradeIconUrl(selectedIndex); // NEW

  return (
    <div className="mh-card">
      <div className="mh-card-header">
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {iconUrl && (
            <img
              src={iconUrl}
              alt={meta.displayName}
              width={40}
              height={40}
              style={{ imageRendering: "pixelated" }}
            />
          )}
          <h2 style={{ margin: 0 }}>Upgrade Details</h2>
        </div>

        <select
          value={selectedIndex}
          onChange={(e) => setSelectedIndex(Number(e.target.value))}
          className="mh-select"
        >
          {MINEHEAD_UPGRADE_INDICES.map((idx) => (
            <option key={idx} value={idx}>
              {idx} — {metaLabel(idx)}
            </option>
          ))}
        </select>
      </div>

      <div className="mh-grid">
        <InfoRow label="Key" value={meta.key} />
        <InfoRow label="Display name" value={meta.displayName} />
        <InfoRow label="Level" value={String(level)} />
        <InfoRow
          label="Max level"
          value={meta.maxLevel === null ? "—" : String(meta.maxLevel)}
        />
        <InfoRow
          label="Multiplier"
          value={meta.multiplier === null ? "—" : String(meta.multiplier)}
        />
      </div>

      <div style={{ marginTop: 12, opacity: 0.8, fontSize: 13 }}>
        {meta.notes
          ? meta.notes
          : "Populate max level / multiplier from MineheadUPG to complete this panel."}
      </div>
    </div>
  );
}
function metaLabel(idx: number): string {
  const m = MINEHEAD_UPGRADE_META[idx];
  return m?.displayName ?? mineheadUpgradeName(idx);
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="mh-row">
      <div className="mh-row-k">{label}</div>
      <div className="mh-row-v">{value}</div>
    </div>
  );
}