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

function parseCsvLine(line) {
  const values = [];
  let rest = line;
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
  return values;
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

  const lines = fs
    .readFileSync(path.join(root, "data", "arithmetic-tasks-medium-5-6.csv"), "utf8")
    .split(/\r?\n/)
    .filter(Boolean);
  const headers = parseCsvLine(lines[0]);
  const rows = lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row = {};
    headers.forEach((h, i) => {
      row[h] = values[i] ?? "";
    });
    return row;
  });

  const { data: existing, error: selectError } = await supabase
    .from("arithmetic_tasks")
    .select("question")
    .eq("level", "Средний");
  if (selectError) {
    console.log("SELECT_ERR", selectError.message);
    process.exit(1);
  }
  const have = new Set((existing || []).map((r) => r.question));
  const toInsert = rows
    .filter((r) => !have.has(r.question))
    .map((r) => ({
      subject: r.subject,
      class_name: r.class_name,
      level: r.level,
      question: r.question,
      answer: r.answer,
      image: r.image,
      explanation_of_the_answer: r.explanation_of_the_answer,
    }));

  console.log("EXISTING", have.size, "TO_INSERT", toInsert.length);
  if (!toInsert.length) {
    return;
  }

  const { error: insertError } = await supabase
    .from("arithmetic_tasks")
    .insert(toInsert);
  if (insertError) {
    console.log("INSERT_ERR", insertError.message);
    process.exit(1);
  }
  console.log("INSERTED", toInsert.length);
}

main().catch((err) => {
  console.log("CRASH", err.message);
  process.exit(1);
});
