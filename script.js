import fs from "node:fs";
import { spawnSync } from "node:child_process";

const SECRET_NAME = "face-blur";
const ENV_FILE = ".env";

const env = fs.readFileSync(ENV_FILE, "utf8");

const args = ["secret", "create", SECRET_NAME];

for (const line of env.split(/\r?\n/)) {
  const trimmed = line.trim();

  if (!trimmed || trimmed.startsWith("#")) continue;

  const idx = trimmed.indexOf("=");
  if (idx === -1) continue;

  const key = trimmed.slice(0, idx).trim();
  const value = trimmed.slice(idx + 1);

  args.push(`${key}=${value}`);
}

console.log(`Creating Modal secret "${SECRET_NAME}"...`);

const result = spawnSync("modal", args, {
  stdio: "inherit",
});

process.exit(result.status ?? 1);