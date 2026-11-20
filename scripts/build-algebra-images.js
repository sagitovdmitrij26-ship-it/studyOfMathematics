const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

const root = path.join(__dirname, "..");
const tasksDir = path.join(root, "public", "tasks");

const files = [
  {
    csv: "algebra-7-basic.csv",
    prefix: "al-b",
    accent: "#2f6b4f",
    paper: "#e8f6ee",
    ink: "#1c3d2e",
  },
  {
    csv: "algebra-7-medium.csv",
    prefix: "al-m",
    accent: "#8a6a12",
    paper: "#fff6d6",
    ink: "#4a3a08",
  },
  {
    csv: "algebra-7-high.csv",
    prefix: "al-h",
    accent: "#9a4a28",
    paper: "#ffe8dc",
    ink: "#4a2214",
  },
];

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

function csvEscape(value) {
  const text = String(value ?? "");
  if (/[",\n]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function wrapText(text, maxChars) {
  const words = text.split(/\s+/);
  const lines = [];
  let current = "";
  for (const word of words) {
    const next = current ? `${current} ${word}` : word;
    if (next.length > maxChars && current) {
      lines.push(current);
      current = word;
    } else {
      current = next;
    }
  }
  if (current) {
    lines.push(current);
  }
  return lines.slice(0, 5);
}

function escapeXml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formulaFromQuestion(question) {
  const q = question.replace(/^"|"$/g, "").trim();
  const afterColon = q.split(":").slice(1).join(":").trim();
  if (afterColon) {
    return afterColon.replace(/\s+Найдите\s+[xy]\.?$/i, "").trim();
  }
  return q.replace(/^Найдите значение( выражения)?\s+/i, "").trim();
}

function makeSvg({ question, level, index, total, accent, paper, ink }) {
  const formula = formulaFromQuestion(question);
  const lines = wrapText(formula, 28);
  const fontSize = lines.some((line) => line.length > 24) ? 28 : 36;
  const startY = 268 - ((lines.length - 1) * (fontSize + 10)) / 2;
  const tspan = lines
    .map((line, i) => {
      const dy = i === 0 ? 0 : fontSize + 10;
      return `<tspan x="480" dy="${dy}">${escapeXml(line)}</tspan>`;
    })
    .join("");

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
  <rect width="960" height="540" rx="28" fill="${paper}"/>
  <rect x="36" y="36" width="888" height="468" rx="18" fill="#fffdf8" stroke="${accent}" stroke-width="3"/>
  <path d="M36 120 H924" stroke="${accent}" stroke-opacity="0.35" stroke-width="2"/>
  <circle cx="88" cy="78" r="18" fill="${accent}"/>
  <text x="88" y="85" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#fff">x</text>
  <text x="128" y="86" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="700" fill="${ink}">Алгебра · 7 класс</text>
  <text x="880" y="86" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="20" fill="${accent}">${escapeXml(level)} · ${index}/${total}</text>
  <text x="480" y="${startY}" text-anchor="middle" font-family="Georgia, serif" font-size="${fontSize}" fill="${ink}">${tspan}</text>
  <text x="480" y="455" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="18" fill="${accent}">Матеум · тренажёр</text>
</svg>
`;
}

async function main() {
  fs.mkdirSync(tasksDir, { recursive: true });
  const allRows = [];

  for (const spec of files) {
    const csvPath = path.join(root, "data", spec.csv);
    const raw = fs.readFileSync(csvPath, "utf8");
    const lines = raw.split(/\r?\n/).filter(Boolean);
    const headers = parseCsvLine(lines[0]);
    const rows = lines.slice(1).map((line) => {
      const values = parseCsvLine(line);
      const row = {};
      headers.forEach((h, i) => {
        row[h] = values[i] ?? "";
      });
      return row;
    });

    rows.forEach((row, i) => {
      const num = String(i + 1).padStart(2, "0");
      const fileName = `${spec.prefix}-${num}.svg`;
      const imagePath = `/tasks/${fileName}`;
      fs.writeFileSync(
        path.join(tasksDir, fileName),
        makeSvg({
          question: row.question,
          level: row.level,
          index: i + 1,
          total: rows.length,
          accent: spec.accent,
          paper: spec.paper,
          ink: spec.ink,
        }),
        "utf8"
      );
      row.image = imagePath;
      allRows.push(row);
    });

    const out = [
      headers.join(","),
      ...rows.map((row) => headers.map((h) => csvEscape(row[h])).join(",")),
    ].join("\n");
    fs.writeFileSync(csvPath, `${out}\n`, "utf8");
    console.log("CSV", spec.csv, rows.length);
  }

  const env = {
    ...parseEnv(path.join(root, ".env")),
    ...parseEnv(path.join(root, ".env.local")),
  };
  const url = env.REACT_APP_SUPABASE_URL;
  const key = env.REACT_APP_SUPABASE_ANON_KEY;
  if (!url || !key) {
    console.log("NO_ENV");
    return;
  }

  const supabase = createClient(url, key);
  const { data, error } = await supabase
    .from("arithmetic_tasks")
    .select("id, question, level")
    .eq("subject", "algebra")
    .order("id");
  if (error) {
    console.log("SELECT_ERR", error.message);
    return;
  }

  let ok = 0;
  let fail = 0;
  for (const csvRow of allRows) {
    const match = (data || []).find(
      (row) => row.question === csvRow.question && row.level === csvRow.level
    );
    if (!match) {
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
  console.log("UPDATED", ok, "FAILED", fail, "TOTAL_CSV", allRows.length);
}

main().catch((err) => {
  console.log("CRASH", err.message);
  process.exit(1);
});
