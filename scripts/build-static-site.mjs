import { cp, lstat, mkdir, mkdtemp, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const slidesDir = resolve(root, "slides");
const siteDir = resolve(root, "site");
const markerPath = resolve(siteDir, ".marp-site-generated");
const marpCliPath = resolve(root, "node_modules", "@marp-team", "marp-cli", "marp-cli.js");
const chapterPattern = /^第(\d+)章_.+_100页_Marp\.md$/;

function run(command, args) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(command, args, { cwd: root, stdio: "inherit" });
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) resolvePromise();
      else reject(new Error(`${command} exited with code ${code}`));
    });
  });
}

async function createThemeSet() {
  const themeDirectory = await mkdtemp(resolve(tmpdir(), "marp-themes-"));
  const template = (await readFile(resolve(root, "themes", "am_template.scss"), "utf8"))
    .replace("/* @theme am_template */", "");
  const themeFiles = (await readdir(resolve(root, "themes")))
    .filter((filename) => filename.startsWith("am_") && filename !== "am_template.scss");

  await Promise.all(themeFiles.map(async (filename) => {
    const source = await readFile(resolve(root, "themes", filename), "utf8");
    const bundledTheme = source.replace("@import 'am_template';", template);
    await writeFile(resolve(themeDirectory, filename.replace(/\.scss$/, ".css")), bundledTheme, "utf8");
  }));
  return themeDirectory;
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[character]);
}

async function prepareSiteDirectory() {
  try {
    await lstat(siteDir);
  } catch {
    await mkdir(siteDir, { recursive: true });
    return;
  }

  try {
    await lstat(markerPath);
  } catch {
    throw new Error("site/ already exists but is not a generated site. Move or review its contents before rebuilding.");
  }

  await rm(siteDir, { recursive: true, force: true });
  await mkdir(siteDir, { recursive: true });
}

async function getChapters() {
  const entries = await readdir(slidesDir);
  const chapters = [];
  for (const filename of entries) {
    const match = filename.match(chapterPattern);
    if (!match) continue;
    const source = resolve(slidesDir, filename);
    const content = await readFile(source, "utf8");
    const firstTitle = content.match(/^#\s+(.+)$/m)?.[1]?.trim() ?? `第${Number(match[1])}章`;
    chapters.push({ number: Number(match[1]), filename, source, title: firstTitle, content });
  }
  return chapters.sort((a, b) => a.number - b.number);
}

function createIndex(chapters) {
  const cards = chapters.map(({ number, title, filename }) => {
    const chapterId = `ch${String(number).padStart(2, "0")}`;
    return `\n      <a class="chapter-card" href="${chapterId}/" aria-label="打开${escapeHtml(title)}">\n        <span class="chapter-number">${String(number).padStart(2, "0")}</span>\n        <span class="chapter-title">${escapeHtml(title)}</span>\n        <span class="chapter-source">${escapeHtml(filename)}</span>\n      </a>`;
  }).join("");

  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="人工智能与大数据课程静态课件">
  <title>人工智能与大数据｜课程课件</title>
  <style>
    :root { color-scheme: light; font-family: "Microsoft YaHei", "Noto Sans SC", Arial, sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; color: #173b31; background: linear-gradient(145deg, #edf7f1 0%, #ffffff 55%, #e1f1e8 100%); }
    main { width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 72px 0; }
    .eyebrow { margin: 0 0 12px; color: #20784e; font-size: 14px; font-weight: 700; letter-spacing: .12em; }
    h1 { max-width: 760px; margin: 0; font-size: clamp(34px, 6vw, 62px); line-height: 1.12; }
    .intro { max-width: 700px; margin: 20px 0 44px; color: #4e665d; font-size: 18px; line-height: 1.8; }
    .chapter-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 18px; }
    .chapter-card { display: grid; grid-template-columns: auto 1fr; gap: 6px 14px; min-height: 150px; padding: 24px; color: inherit; text-decoration: none; border: 1px solid #cfe3d8; border-radius: 18px; background: rgba(255,255,255,.92); box-shadow: 0 8px 28px rgba(27, 83, 57, .08); transition: transform .16s ease, box-shadow .16s ease; }
    .chapter-card:hover, .chapter-card:focus-visible { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(27, 83, 57, .16); outline: 3px solid #78bd98; outline-offset: 3px; }
    .chapter-number { color: #258152; font-size: 14px; font-weight: 800; letter-spacing: .08em; }
    .chapter-title { align-self: center; font-size: 19px; font-weight: 700; line-height: 1.45; }
    .chapter-source { grid-column: 1 / -1; overflow: hidden; color: #71867c; font-size: 12px; text-overflow: ellipsis; white-space: nowrap; }
    footer { margin-top: 48px; color: #6e8279; font-size: 14px; }
    @media (max-width: 600px) { main { width: min(100% - 28px, 1120px); padding: 48px 0; } .intro { font-size: 16px; } }
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">NJUST · COURSE MATERIALS</p>
    <h1>人工智能与大数据</h1>
    <p class="intro">课程课件静态网页。选择章节后，可在浏览器中逐页浏览、全屏演示或打印课件。</p>
    <nav class="chapter-grid" aria-label="课程章节">${cards}
    </nav>
    <footer>南京理工大学 · Shiyan Pan</footer>
  </main>
</body>
</html>`;
}

async function main() {
  const chapters = await getChapters();
  if (chapters.length !== 10) throw new Error(`Expected 10 chapter files, found ${chapters.length}.`);

  await prepareSiteDirectory();
  const themeDirectory = await createThemeSet();
  const localAssetDirectories = ["assets", "images", "files"];
  const copiedDirectories = localAssetDirectories.filter((directory) => {
    const referencePattern = new RegExp(`!\\[[^\\]]*\\]\\([^)]*(?:\\.\\./)?${directory}/|<img[^>]+src=["'][^"']*(?:\\.\\./)?${directory}/`, "i");
    return chapters.some(({ content }) => referencePattern.test(content));
  });
  await Promise.all(copiedDirectories.map((directory) =>
    cp(resolve(root, directory), resolve(siteDir, directory), { recursive: true, force: true })
  ));

  try {
    for (const chapter of chapters) {
      const chapterId = `ch${String(chapter.number).padStart(2, "0")}`;
      const outputDir = resolve(siteDir, chapterId);
      await mkdir(outputDir, { recursive: true });
      await run(process.execPath, [marpCliPath, "--theme-set", themeDirectory, "--html", "--allow-local-files", "--output", resolve(outputDir, "index.html"), relative(root, chapter.source)]);
    }
  } finally {
    await rm(themeDirectory, { recursive: true, force: true });
  }

  await writeFile(resolve(siteDir, "index.html"), createIndex(chapters), "utf8");
  await writeFile(resolve(siteDir, "CNAME"), "ai-bigdata-course.shiyanpan.cn\n", "utf8");
  await writeFile(resolve(siteDir, ".nojekyll"), "Generated static site.\n", "utf8");
  await writeFile(markerPath, "Generated by npm run build:site. Do not edit manually.\n", "utf8");
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
