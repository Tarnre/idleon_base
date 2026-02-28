export type ResearchBlob = unknown[][];

/**
 * The exported config.json stores "Research" as a JSON-encoded string.
 * This parses:
 *   config["Research"] -> string -> JSON.parse -> list of lists
 */
export function parseResearchFromConfig(rawConfig: unknown): ResearchBlob | null {
  if (!rawConfig || typeof rawConfig !== "object") return null;

  const researchValue = (rawConfig as Record<string, unknown>)["Research"];
  if (typeof researchValue !== "string") return null;

  let decoded: unknown;
  try {
    decoded = JSON.parse(researchValue);
  } catch {
    return null;
  }

  if (!Array.isArray(decoded)) return null;

  const blob: unknown[][] = [];
  for (const item of decoded) {
    blob.push(Array.isArray(item) ? (item as unknown[]) : []);
  }
  return blob;
}