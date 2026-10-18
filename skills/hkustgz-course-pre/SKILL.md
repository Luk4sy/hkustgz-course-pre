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
4. **Respect the time limit.** About 140 words per minute of spoken English. Plan the spoken part to fill at most **90% of the slot**, leaving room for clicks, a slow start and nerves. An 8-minute talk is about 1,000 words and 9–12 slides.
5. **When the user asks for text only ("发给我就行"), send the text and do not edit files.**
6. **Never download copyrighted video from YouTube or similar sites.** Ask the user to screen-record the clip and upload it.
7. **No unsourced facts.** Every number or claim on a slide or in the notes comes from the user's material or a source you opened. If something is unknown, say so; don't fill the gap.
8. **Keep private details out.** Course requirements are given by the user each time; don't store instructor or classmate information in the skill.

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

Produce the plan as one table, one row per slide, following the matching playbook:

| # | Slide ID | Audience sees | I say (3–5 points) | Time | Transition to next |
|---|---|---|---|---|---|
| 1 | `cover` | title, authors, venue, video | who / what / why it matters | 0:40 | "So what problem are they solving?" |

- **Slide ID**: a short stable slug (`cover`, `motivation`, `method`, `results-energy`, `verdict`), never a page number. Notes and build code are keyed by it, so reordering slides can't attach notes to the wrong page.
- **Audience sees** is what is on the slide; **I say** is what only the speaker adds. If the two columns say the same thing, the slide has too much text.
- **Time** column total ≤ 90% of the limit; show the total under the table.
- **Transition** is one spoken sentence that hands over to the next slide. Every row has one except the last.
- Rhythm: no three dense slides in a row; a big-number, image or section slide every 3–4 slides.

Agree on the table with the user, then wait for "开动". The notes are written from the "I say" and "Transition" columns.

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
python scripts/check_deck.py final.pptx --minutes 8
```

Never pipe these scripts into `head`; a broken pipe can truncate the output file.

## Step 5 — QA

- Render: `soffice --headless --convert-to pdf`, then `pdftoppm -r 50` and check a contact sheet for overflow, overlap and the logo on every slide.
- Run the pptx skill's `validate.py`. If it reports an undeclared `jpg` extension, add `<Default Extension="jpg" ContentType="image/jpeg"/>` to `[Content_Types].xml`.
- Run `python scripts/check_deck.py final.pptx --minutes <limit>`. It fails if a slide's `[CLICK]` markers don't match its click steps, a slide has no notes, or the spoken time is over 90% of the limit (it says how many words to cut).
- Instructor's required items are on the opening slides.

## Step 6 — Deliver

- Save the .pptx into the user's connected folder (or send it in chat).
- Tell them how to use presenter mode (WPS: 放映 → 演讲者视图 / 设置放映方式 → 显示演讲者视图; PowerPoint: Slide Show → Use Presenter View).
- Offer: notes as plain text, a rehearsal run-through, or Q&A prep (Step 7).

## Step 7 — Q&A prep (offer after every deck; do it when asked)

Predict the **5 most likely questions** for this talk and prepare an answer for each. Give them in the user's language, with the answer itself in the slide language.

For each question give:

- **The question**, phrased the way a classmate or the instructor would ask it.
- **A 30-second answer**: the point first, then one piece of evidence.
- **Where the evidence is**: the slide ID, or "not in the deck" (then suggest a backup slide).
- **If you don't know**: one honest fallback sentence ("The paper doesn't report that; my guess is … because …").

Where questions come from, by talk type:

- **Author**: limitations you'd rather not discuss, baselines and comparisons, whether it generalizes, cost or practicality.
- **Reviewer**: "Is your criticism fair?", "Would you accept it anyway?", "What experiment would fix it?" The audience tests the critique, not the paper.
- **Researcher**: feasibility, why this metric or sample size, what if the result is negative, how it differs from the original paper.
- **Project / proposal**: what you'd do with more time, why this approach over an obvious alternative, risks.
- **Group**: who did which part; make sure each member can answer one question.
- **Topic / case analysis**: the strongest counter-argument, a stakeholder you left out, whether the lesson transfers elsewhere.

Mark the hardest question and offer one backup slide for it (placed after the closing slide, hidden from the main flow). Facts in answers follow principle 7: nothing unsourced.
