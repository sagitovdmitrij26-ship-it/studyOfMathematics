const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

function parseEnv(filePath) {
  const out = {};
  if (!fs.existsSync(filePath)) {
    return out;
  }
  for (const line of fs.readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }
    const i = trimmed.indexOf("=");
    if (i < 0) {
      continue;
    }
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

function parseCsv(filePath) {
  const text = fs.readFileSync(filePath, "utf8");
  const lines = text.split(/\r?\n/).filter(Boolean);
  const headers = [];
  let headerRest = lines[0];
  while (headerRest.length) {
    const comma = headerRest.indexOf(",");
    if (comma < 0) {
      headers.push(headerRest);
      break;
    }
    headers.push(headerRest.slice(0, comma));
    headerRest = headerRest.slice(comma + 1);
  }
  const rows = [];
  for (let n = 1; n < lines.length; n += 1) {
    const values = [];
    let rest = lines[n];
    while (rest.length) {
      if (rest[0] === '"') {
        let end = 1;
        let cell = "";
        while (end < rest.length) {
          if (rest[end] === '"' && rest[end + 1] === '"') {
            cell += '"';
            end += 2;
            continue;
          }
          if (rest[end] === '"') {
            end += 1;
            break;
          }
          cell += rest[end];
          end += 1;
        }
        values.push(cell);
        rest = rest[end] === "," ? rest.slice(end + 1) : rest.slice(end);
      } else {
        const comma = rest.indexOf(",");
        if (comma < 0) {
          values.push(rest);
          rest = "";
        } else {
          values.push(rest.slice(0, comma));
          rest = rest.slice(comma + 1);
        }
      }
    }
    const row = {};
    headers.forEach((h, i) => {
      row[h] = values[i] ?? "";
    });
    rows.push(row);
  }
  return rows;
}

async function main() {
  const root = path.join(__dirname, "..");
  const env = {
    ...parseEnv(path.join(root, ".env")),
    ...parseEnv(path.join(root, ".env.local")),
  };
  const url = env.REACT_APP_SUPABASE_URL;
  const key = env.REACT_APP_SUPABASE_ANON_KEY;
  if (!url || !key) {
    console.log("NO_ENV");
    process.exit(1);
  }

  const csvRows = parseCsv(
    path.join(root, "data", "arithmetic-tasks-medium-5-6.csv")
  );
  const supabase = createClient(url, key);
  const { data, error } = await supabase
    .from("arithmetic_tasks")
    .select("id, question, image, level")
    .eq("level", "Средний")
    .order("id");

  if (error) {
    console.log("SELECT_ERR", error.message);
    process.exit(1);
  }

  console.log("MEDIUM_COUNT", (data || []).length);

  let ok = 0;
  let fail = 0;
  for (const csvRow of csvRows) {
    const match = (data || []).find((row) => row.question === csvRow.question);
    if (!match) {
      console.log("NO_MATCH", csvRow.question.slice(0, 50));
      fail += 1;
      continue;
    }
    const { error: updateError } = await supabase
      .from("arithmetic_tasks")
      .update({ image: csvRow.image })
      .eq("id", match.id);
    if (updateError) {
      console.log("UPDATE_ERR", updateError.message);
      fail += 1;
      break;
    }
    ok += 1;
  }
  console.log("UPDATED", ok, "FAILED", fail);
}

main().catch((err) => {
  console.log("CRASH", err.message);
  process.exit(1);
});
