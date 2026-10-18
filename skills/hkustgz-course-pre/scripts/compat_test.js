// Build a small test deck that checks what PowerPoint and WPS each support.
//
// Usage:
//   ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 -pix_fmt yuv420p -c:v libx264 test.mp4
//   ffmpeg -i test.mp4 -frames:v 1 test_poster.png
//   NODE_PATH=$(npm root -g) node compat_test.js test.mp4 test_poster.png compat_raw.pptx
//   python animate.py compat_raw.pptx compat_anim.pptx --video-ms 5000
//   python fixnotes.py compat_anim.pptx compat_notes.pptx
//   python fix_fonts.py compat_notes.pptx compat_fonts.pptx
//   python add_logo.py compat_fonts.pptx compat_test.pptx --color logo_color.png --white logo_white.png
//
// Open compat_test.pptx in each app, go through the slides in presenter view,
// and note which checks pass. Each slide says what "pass" looks like.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const [video, poster, out = "compat_raw.pptx"] = process.argv.slice(2);

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const INK = "1F2937", QUIET = "6B7280", ACCENT = "2563EB";

function header(s, n, title, pass) {
  s.addText(`Test ${n}`, { x: 0.6, y: 0.4, w: 4, h: 0.4, fontFace: "Arial", fontSize: 14, color: ACCENT, bold: true });
  s.addText(title, { x: 0.6, y: 0.8, w: 9, h: 0.8, fontFace: "Arial", fontSize: 30, color: INK, bold: true });
  s.addText(`PASS if: ${pass}`, { x: 0.6, y: 6.6, w: 12, h: 0.5, fontFace: "Arial", fontSize: 14, color: QUIET });
}

// 1. Fonts
{
  const s = pptx.addSlide();
  header(s, 1, "Fonts / 字体", "every line shows its own font, no boxes or fallback to a serif font");
  const rows = [
    ["Arial — The quick brown fox", "Arial"],
    ["Calibri — The quick brown fox", "Calibri"],
    ["Cambria — The quick brown fox", "Cambria"],
    ["微软雅黑 Microsoft YaHei — 港科广课程汇报", "Microsoft YaHei"],
    ["等线 DengXian — 港科广课程汇报", "DengXian"],
    ["苹方 PingFang SC — 港科广课程汇报", "PingFang SC"],
    ["思源黑体 Source Han Sans SC — 港科广课程汇报", "Source Han Sans SC"],
    ["Arial box with Chinese 中文混排 — 港科广课程汇报", "Arial"],
  ];
  rows.forEach(([t, f], i) => s.addText(t, { x: 0.6, y: 1.75 + i * 0.6, w: 12, h: 0.5, fontFace: f, fontSize: 22, color: INK }));
  s.addNotes("Slide 1: fonts.\n第 1 页：字体。\nWrite down any line that looks wrong in this app.\n记下在这个软件里显示不对的行。");
}

// 2. Notes
{
  const s = pptx.addSlide();
  header(s, 2, "Speaker notes / 备注", "in presenter view, the notes show as separate lines, English and Chinese alternating");
  s.addText("Open presenter view and look at the notes panel.\n打开演讲者视图，看备注栏。", { x: 0.6, y: 2.2, w: 12, h: 1.4, fontFace: "Arial", fontSize: 24, color: INK });
  s.addNotes("Line 1 in English.\n第一行，中文。\nLine 2 in English.\n第二行，中文。\n\nAfter a blank line.\n空行之后。");
}

// 3. Click animations
{
  const s = pptx.addSlide();
  header(s, 3, "Click animations / 点击动画", "the three boxes fade in one per click, in order 1 → 2 → 3");
  [1, 2, 3].forEach((n, i) => {
    s.addShape(pptx.ShapeType.roundRect, { x: 0.6 + i * 4.1, y: 2.4, w: 3.7, h: 2.4, fill: { color: "DBEAFE" }, line: { color: ACCENT, width: 1.5 }, rectRadius: 0.1, objectName: `a${n}_box` });
    s.addText(String(n), { x: 0.6 + i * 4.1, y: 2.4, w: 3.7, h: 2.4, align: "center", valign: "middle", fontFace: "Arial", fontSize: 60, color: ACCENT, bold: true, objectName: `a${n}_num` });
  });
  s.addNotes("Nothing is visible yet.\n现在什么都没有。\n[CLICK] Box one.\n【点击】第一个。\n[CLICK] Box two.\n【点击】第二个。\n[CLICK] Box three.\n【点击】第三个。");
}

// 4. Video
if (video) {
  const s = pptx.addSlide();
  header(s, 4, "Video / 视频", "the video starts by itself when the slide opens, muted, and loops; the poster shows in edit mode");
  s.addMedia({ type: "video", path: video, cover: poster ? "data:image/png;base64," + fs.readFileSync(poster).toString("base64") : undefined, x: 3.2, y: 1.8, w: 6.9, h: 3.9 });
  s.addNotes("The video should play on its own.\n视频应该自动播放。\nIf it does not, click it once and note that.\n如果没有，点一下，并记下来。");
}

// 5 + 6. Logo on light and dark backgrounds
{
  const s = pptx.addSlide();
  header(s, 5, "Logo on light background / 浅色背景 logo", "the logo top right has no white box around it");
  s.addNotes("Look at the top right corner.\n看右上角。");
  const d = pptx.addSlide();
  d.background = { color: "111827" };
  d.addText("Test 6", { x: 0.6, y: 0.4, w: 4, h: 0.4, fontFace: "Arial", fontSize: 14, color: "93C5FD", bold: true });
  d.addText("Logo on dark background / 深色背景 logo", { x: 0.6, y: 0.8, w: 9, h: 0.8, fontFace: "Arial", fontSize: 30, color: "FFFFFF", bold: true });
  d.addText("PASS if: the logo top right is white and has no box around it", { x: 0.6, y: 6.6, w: 12, h: 0.5, fontFace: "Arial", fontSize: 14, color: "9CA3AF" });
  d.addNotes("Look at the top right corner.\n看右上角。");
}

// 7. Transitions
{
  const s = pptx.addSlide();
  header(s, 7, "Transitions / 翻页效果", "moving between slides fades instead of cutting");
  s.addText("End of test. Thank you!\n测试结束。", { x: 0.6, y: 2.4, w: 12, h: 1.4, fontFace: "Arial", fontSize: 28, color: INK });
  s.addNotes("Last slide.\n最后一页。");
}

pptx.writeFile({ fileName: out }).then(f => console.log("wrote", f));
