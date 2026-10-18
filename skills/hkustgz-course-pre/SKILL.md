---
name: hkustgz-course-pre
description: Plan and build HKUST(GZ) course presentation slides (.pptx) — paper pres, project progress/final, proposals, group talks, topic or case analysis, demos and short pitches — with bilingual speaker notes, click animations and the school logo.
---

# HKUST(GZ) Course Presentation (课程 Pre)

## 给使用者的一句话说明

把作业要求和材料（论文、报告、数据、图片）交给 Claude。Claude 会先用大白话帮你讲懂内容，再和你一起定"这次 pre 怎么讲"。你说 **"开动"** 之后，它才做出一份能在 WPS / PowerPoint 演讲者模式里直接用的 .pptx。备注里有中英逐字稿，标好了每次该点击的地方。

---

# Technical guide (for the assistant)

## Core principles

1. **Understand → plan → build. Never skip ahead.** Do not write any slide code until the user explicitly says "开动" / "go" / "start building". Before that, only explain and plan.
2. **Plain language first.** Explain the material as if to a smart friend outside the field: one-sentence version, an everyday analogy, then the details. If the user says "还是没讲清楚", simplify again; do not add jargon.
3. **Reply in the user's language** (usually Chinese). Slides and script can be English; the default is English slides with bilingual EN + ZH notes.
4. **Respect the time limit.** About 140 words per minute of spoken English. An 8-minute talk is about 1,100 words and 10–13 slides.
5. **When the user asks for text only ("发给我就行"), send the text and do not edit files.**
6. **Never download copyrighted video from YouTube or similar sites.** Ask the user to screen-record the clip and upload it.

## Step 1 — Collect the brief

Ask (with AskUserQuestion) only what is missing:

- Course code and talk type (see playbooks below); time limit; solo or group (and which part is theirs).
- Required items from the instructor. Some instructors want a fixed opening, e.g. **Title / Authors & Institution / Venue & Year / Intuition or Motivation** at the start of every talk; always honor these.
- Audience: classmates from mixed backgrounds, or specialists.
- Slide language and note language.
- Visual style: a color, or "let me recommend". If several decks are made for different people (e.g. a classmate), use a clearly different style for each.
- Tone: neutral academic, or with light humor. Keep humor light; if the user says it is too much, cut it back hard.
- Related talks on the same day: link them with "just now / in my first talk" wording, never "last time".

## Step 2 — Understand the material

- Find the real source. If only a supplementary file was provided, help locate the main text (publisher page, arXiv / bioRxiv preprint, institutional repository).
- Give: one-sentence summary; the problem and why it matters; what they did (method in plain words); key results with numbers; limitations.
- Check understanding with the user before planning.

## Step 3 — Plan the talk (no slides yet)

Produce a slide-by-slide outline: slide title, the one message of that slide, visual (figure / diagram / video / table), seconds allotted. Follow the matching playbook. Agree on it with the user, then wait for "开动".

## Playbooks

### A. Paper presentation (role-based: Author / Reviewer / Researcher)

Common opening (1–2 slides): instructor's required items, then a hook (video, striking figure or question).

- **Author** — speak as if you wrote it. Motivation → gap → our idea → design / method → key results (2–3 figures max) → limitations we admit → future work → take-home message.
- **Reviewer** — fair critique. Summary in 1 slide → strengths (novelty, rigor, impact) → weaknesses (claims vs evidence, sample size, baselines, generalization, reproducibility) → questions for the authors → verdict (accept / minor / major revision) with reasons.
- **Researcher (create)** — use the paper as a springboard. What it leaves open → your new research question → proposed method / framework diagram → study design (phases, participants, metrics) → expected outcomes and risks → timeline.

### B. Course project — progress report / final presentation

- Progress: goal recap (1 slide) → what is done (with evidence) → what changed from the plan and why → problems and how you are handling them → next steps with dates → what you need from the instructor.
- Final: problem and motivation → approach → results (demo or figures) → evaluation against the original goals → lessons learned → future work. Lead with the result, not the process diary.

### C. Proposal / 开题 / research plan

Background → gap (why existing work is not enough) → research question(s) and objectives → method and data → feasibility (resources, preliminary results) → timeline (Gantt-style) → expected contributions → risks and fallback plans.

### D. Group presentation

- Split by storyline, not by person. Each speaker owns a contiguous section.
- Add explicit hand-offs in notes ("Next, X will show…").
- One shared visual style and terminology; one person checks the whole deck for consistency.
- Mark on the outline who speaks which slides and their time budget.

### E. Topic or case analysis (general, any discipline)

Keep it accessible to non-specialists. A general frame:

1. **What happened / what is the topic** — background in plain words, one key fact or number.
2. **Why it matters** — who is affected, scale, stakes.
3. **Key actors and their views** — a simple map of stakeholders.
4. **Analysis** — pick one simple lens that fits (causes → effects; before vs after; pros vs cons; comparison with another place or case; SWOT). Don't force a technical framework.
5. **Options or lessons** — 2–3 choices or takeaways, with trade-offs.
6. **Your recommendation / conclusion** — and one open question for discussion.

### F. Technical demo / system presentation

Problem → what the system does (one diagram) → live demo or recorded video (always have a backup recording) → how it works (architecture, only what is needed) → evaluation → limitations → next steps.

### G. Short pitch (1–3 minutes)

Hook → problem → solution → why it is credible (evidence) → one clear ask. 3–5 slides, very few words per slide.

## Step 4 — Build the .pptx (only after "开动")

Use the pptx skill (pptxgenjs, `LAYOUT_WIDE` 13.333 × 7.5 in).

- **Design:** one accent color plus neutrals; consistent master layouts; large figures over bullet walls; one message per slide in the title.
- **Figures from PDFs:** render pages at 300–400 dpi (`pdftoppm`) and crop; or extract embedded photos with `pdfimages`. Cite the source under each figure.
- **Video:** embed the user's own screen recording with a poster frame; caption the source. `scripts/animate.py` makes it autoplay muted and loop when the slide opens (verify in WPS; support varies).
- **Click animations:** name shapes `a1_xxx`, `a2_xxx`, … (same number = appears on the same click). `scripts/animate.py` adds fade transitions and fade-in click sequences.
- **Speaker notes:** bilingual, short spoken sentences. Mark each click as `[CLICK]` / `【点击】`; the number of markers must equal the number of click groups on that slide. Run `scripts/fixnotes.py` so each line is its own paragraph (otherwise WPS shows one block).
- **School logo:** top-right of every slide, cut out from its white background. `scripts/logo_cutout.py` makes a transparent color version and a white version; `scripts/add_logo.py` picks color or white per slide from the background brightness and nudges overlapping titles. Users supply their own logo file; do not redistribute it.

Pipeline:

```
node build.js                                   # -> deck.pptx
python scripts/animate.py deck.pptx deck_anim.pptx [--video-ms 5000]
python scripts/fixnotes.py deck_anim.pptx deck_notes.pptx
python scripts/add_logo.py deck_notes.pptx final.pptx --color logo_color.png --white logo_white.png
```

Never pipe these scripts into `head`; a broken pipe can truncate the output file.

## Step 5 — QA

- Render: `soffice --headless --convert-to pdf`, then `pdftoppm -r 50` and check a contact sheet for overflow, overlap and the logo on every slide.
- Run the pptx skill's `validate.py`. If it reports an undeclared `jpg` extension, add `<Default Extension="jpg" ContentType="image/jpeg"/>` to `[Content_Types].xml`.
- Script length: word count ÷ 140 ≈ minutes; must fit the limit.
- `[CLICK]` count per slide = click groups per slide.
- Instructor's required items are on the opening slides.

## Step 6 — Deliver

- Save the .pptx into the user's connected folder (or send it in chat).
- Tell them how to use presenter mode (WPS: 放映 → 演讲者视图 / 设置放映方式 → 显示演讲者视图; PowerPoint: Slide Show → Use Presenter View).
- Offer: notes as plain text, a rehearsal run-through, or a Q&A prep list.
