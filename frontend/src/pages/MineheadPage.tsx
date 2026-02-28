import MineheadStatusBar from "../components/minehead/StatusBar";
import UpgradeDetails from "../components/minehead/UpgradeDetails";
import { useMemo, useState } from "react";
import ConfigUpload from "../components/profile/ConfigUpload";
import { parseResearchFromConfig } from "../domain/world7/research";
import {
  mineheadUpgradeLevel,
  parseMineheadFromResearch,
} from "../domain/world7/mineheadProfile";
import {
  mineheadUpgradeName,
  MINEHEAD_UPGRADE_INDICES,
} from "../domain/world7/mineheadUpgrades";

export default function MineheadPage() {
  const [rawConfig, setRawConfig] = useState<unknown | null>(null);
  const [error, setError] = useState<string>("");

  const research = useMemo(() => {
    if (!rawConfig) return null;
    return parseResearchFromConfig(rawConfig);
  }, [rawConfig]);

  const minehead = useMemo(() => {
    if (!research) return null;
    return parseMineheadFromResearch(research);
  }, [research]);

  return (
    <div style={{ padding: 32, maxWidth: 1100 }}>
      <h1 style={{ marginTop: 0 }}>Minehead Profile Viewer</h1>

      <ConfigUpload
        onLoaded={(raw) => {
          setError("");
          setRawConfig(raw);
        }}
        onError={setError}
      />

      {error && <p style={{ color: "#ff6b6b" }}>{error}</p>}

      {!rawConfig && <p style={{ opacity: 0.8 }}>Upload your config.json to begin.</p>}

      {rawConfig && !research && (
        <p style={{ color: "#ff6b6b" }}>
          Could not parse Research from config.json (missing or invalid Research field).
        </p>
      )}

      {minehead && (
        <>
          <MineheadStatusBar
            opponentIndex={minehead.core.opponentIndex}
            currency={minehead.core.currency}
            lives={null}
            perHour={null}
            baseDmg={null}
            availableUpgrades={null}
          />
          <UpgradeDetails upgrades={minehead.upgrades} />
          <h2>Minehead Core</h2>
          <pre style={preStyle}>{JSON.stringify(minehead.core, null, 2)}</pre>

          <h2>Minehead Upgrades</h2>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Index</th>
                <th style={thStyle}>Name</th>
                <th style={thStyle}>Level</th>
              </tr>
            </thead>
            <tbody>
              {MINEHEAD_UPGRADE_INDICES.map((idx) => (
                <tr key={idx}>
                  <td style={tdStyle}>{idx}</td>
                  <td style={tdStyle}>{mineheadUpgradeName(idx)}</td>
                  <td style={tdStyle}>{mineheadUpgradeLevel(minehead.upgrades, idx)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <details style={{ marginTop: 18 }}>
            <summary style={{ cursor: "pointer" }}>Debug</summary>

            <h3>Upgrades by name</h3>
            <pre style={preStyle}>{JSON.stringify(minehead.upgrades.byName, null, 2)}</pre>

            <h3>Raw Research[7]</h3>
            <pre style={preStyle}>{JSON.stringify(minehead.core.raw, null, 2)}</pre>

            <h3>Raw Research[8]</h3>
            <pre style={preStyle}>{JSON.stringify(minehead.upgrades.raw, null, 2)}</pre>
          </details>
        </>
      )}
    </div>
  );
}

const preStyle: React.CSSProperties = {
  background: "#1a1a1a",
  border: "1px solid #2a2a2a",
  borderRadius: 12,
  padding: 14,
  overflow: "auto",
};

const tableStyle: React.CSSProperties = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: 10,
};

const thStyle: React.CSSProperties = {
  textAlign: "left",
  borderBottom: "1px solid #333",
  padding: "10px 8px",
};

const tdStyle: React.CSSProperties = {
  borderBottom: "1px solid #222",
  padding: "8px",
};