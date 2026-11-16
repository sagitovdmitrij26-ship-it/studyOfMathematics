const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

function parseEnv(filePath) {
  const out = {};
  if (!fs.existsSync(filePath)) return out;
  for (const line of fs.readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const i = trimmed.indexOf("=");
    if (i < 0) continue;
    let value = trimmed.slice(i + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    out[trimmed.slice(0, i).trim()] = value;
  }
  return out;
}

async function main() {
  const root = path.join(__dirname, "..");
  const env = {
    ...parseEnv(path.join(root, ".env")),
    ...parseEnv(path.join(root, ".env.local")),
  };
  const supabase = createClient(
    env.REACT_APP_SUPABASE_URL,
    env.REACT_APP_SUPABASE_ANON_KEY
  );
  const { data, error, count } = await supabase
    .from("arithmetic_tasks")
    .select("id,level,image,question", { count: "exact" })
    .order("id");
  if (error) {
    console.log("ERR", error.message);
    return;
  }
  console.log("TOTAL", count, "FETCHED", (data || []).length);
  const levels = {};
  for (const row of data || []) {
    levels[row.level] = (levels[row.level] || 0) + 1;
  }
  console.log("LEVELS", JSON.stringify(levels));
  const last = (data || []).slice(-3);
  console.log(
    "LAST",
    last.map((r) => ({
      id: r.id,
      level: r.level,
      image: r.image,
      q: r.question.slice(0, 40),
    }))
  );
}

main();
