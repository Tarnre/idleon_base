import { useRef } from "react";

type Props = {
  onLoaded: (raw: unknown) => void;
  onError: (message: string) => void;
};

export default function ConfigUpload({ onLoaded, onError }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const onPick = () => inputRef.current?.click();

  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const raw = JSON.parse(text) as unknown;
      onLoaded(raw);
    } catch (err) {
      onError(`Failed to read/parse JSON: ${String(err)}`);
    } finally {
      // Allow re-uploading same file
      e.target.value = "";
    }
  };

  return (
    <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
      <input
        ref={inputRef}
        type="file"
        accept="application/json,.json"
        onChange={onChange}
        style={{ display: "none" }}
      />
      <button onClick={onPick} style={buttonStyle}>
        Upload config.json
      </button>
      <span style={{ opacity: 0.8 }}>Local only, never uploaded anywhere.</span>
    </div>
  );
}

const buttonStyle: React.CSSProperties = {
  background: "#2b6cff",
  border: "none",
  color: "white",
  padding: "10px 14px",
  borderRadius: 10,
  cursor: "pointer",
  fontWeight: 600,
};