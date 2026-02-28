type StatPillProps = {
  icon: React.ReactNode;
  value: string;
  label: string;
  title?: string;
};

function StatPill({ icon, value, label, title }: StatPillProps) {
  return (
    <div className="mh-pill" title={title}>
      <div className="mh-pill-icon">{icon}</div>
      <div className="mh-pill-text">
        <div className="mh-pill-value">{value}</div>
        <div className="mh-pill-label">{label}</div>
      </div>
    </div>
  );
}

export type MineheadStatusBarProps = {
  lives?: number | null;
  perHour?: number | null;
  baseDmg?: number | null;
  availableUpgrades?: number | null;
  opponentIndex?: number | null;
  currency?: number | null;
};

export default function MineheadStatusBar(props: MineheadStatusBarProps) {
  const lives = props.lives ?? null;
  const perHour = props.perHour ?? null;
  const baseDmg = props.baseDmg ?? null;
  const availableUpgrades = props.availableUpgrades ?? null;

  const opponentIndex = props.opponentIndex ?? null;
  const currency = props.currency ?? null;

  return (
    <div className="mh-statusbar">
      <div className="mh-statusbar-row">
        <StatPill
          icon="♥"
          value={lives === null ? "—" : String(lives)}
          label="Lives"
          title="Minehead lives (decoded later from core slots / upgrades)"
        />
        <StatPill
          icon="❄"
          value={perHour === null ? "—/hr" : `${perHour}/hr`}
          label="Rate"
          title="Minehead gain rate (decode later)"
        />
        <StatPill
          icon="⛏"
          value={baseDmg === null ? "—" : String(baseDmg)}
          label="Base DMG"
          title="Base DMG (requires bonuses parsing + formula wiring)"
        />
        <StatPill
          icon="⬆"
          value={availableUpgrades === null ? "—" : String(availableUpgrades)}
          label="Available Upgrades"
          title="Count of upgrades currently available (decode later)"
        />
      </div>

      <div className="mh-statusbar-row mh-statusbar-subrow">
        <div className="mh-subinfo">
          <span className="mh-subinfo-k">Opponent</span>
          <span className="mh-subinfo-v">
            {opponentIndex === null ? "—" : String(opponentIndex)}
          </span>
        </div>
        <div className="mh-subinfo">
          <span className="mh-subinfo-k">Currency</span>
          <span className="mh-subinfo-v">
            {currency === null ? "—" : String(Math.floor(currency))}
          </span>
        </div>
      </div>
    </div>
  );
}