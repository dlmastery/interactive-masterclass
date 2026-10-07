# Interactive Masterclass

Reusable AI teaching skills, an evidence-based authoring process, and an interactive PCA course built with **native marimo-studio notebooks and slides**.

The aim is to help a learner build a mental model, justify it, use it, recognize its limits, and explain it to someone else. The process covers accessible intuition through research-level judgment. It treats rigorous derivation, useful interaction, illustrations, and spoken explanation as one teaching task.

**Current status — 7 October 2026:** the version 3.1 skill bundle and complete generated development archive are published. The earlier PCA course is preserved as a historical baseline. A new PCA rebuild is starting under the updated process; the baseline has **not** passed the new teaching standard. Neither AI reviews nor software tests establish human learning or superiority to other tutorials.

## Start here

| What you need | Where to go |
|---|---|
| Canonical teaching workflow | [build-interactive-masterclass](skills/build-interactive-masterclass/SKILL.md) |
| Compatible intuition-first entrypoint | [build-intuition-masterclass](skills/build-intuition-masterclass/SKILL.md) |
| Research and coding labs | [build-research-codelabs](skills/build-research-codelabs/SKILL.md) |
| Latest retrospective and exact skill deltas | [Version 3.1 report](outputs/tutor-retrospective-v3-1/REPORT.html), [diffs](outputs/tutor-retrospective-v3-1/v3-to-v3-1.patch), [handoff](outputs/tutor-retrospective-v3-1/HANDOFF.txt) |
| Full retrospective and process design | [Version 3 report](outputs/tutor-retrospective-v3/REPORT.html) |
| Earlier course and launch instructions | [Historical PCA course](outputs/pca-studio/README.md) |
| Original first-version recovery | [Recovery record](outputs/pca-studio/original-first-version/README.md) |
| Video discovery inventory | [31 PCA candidates and access limits](work/tutor-retrospective-v3/pca-video-candidates.md) |
| Creator practice research, including Welch Labs | [Explanatory craft](skills/build-interactive-masterclass/references/explainer-craft.md) |
| What was exported or excluded | [Archive manifest](archive-export-manifest.json) |

GitHub shows HTML as source. To read the rendered reports locally, run `python -m http.server 8080` from the repository root and open `http://localhost:8080/outputs/tutor-retrospective-v3-1/REPORT.html`. This serves the reports; it does not start the interactive notebook course.

## Install the skills

Copy the **three directories** under `skills/` into your coding agent's personal skill directory. For Codex, the default is `~/.codex/skills/`. Keep them side by side because the two companion skills link to the canonical skill. Preserve a backup before replacing an existing installation.

Examples of requests:

> Use build-interactive-masterclass to create a native marimo-studio course on PCA for an undergraduate. Start with a grounded geometric problem, then derive the method. Introduce prerequisites at the point of use. Follow the research, pilot, interaction, narration, and review requirements. Complete the full authorized course after the pilot.

> Use build-interactive-masterclass to review a proposed tutorial on a historical topic. Assess purpose, evidence, interpretation, audience adaptation, and transfer. This request is a review only; do not build the course.

> Use build-research-codelabs to design a research-grounded masterclass with executable experiments, laptop defaults, larger-compute extensions, clear provenance, and useful failure diagnosis.

The skill supports several media. It does not require marimo for every topic or turn a short question into a large production project.

## What the teaching process requires

1. **Purpose and learner capabilities.** Establish why the topic matters and what the learner will be able to explain or decide.
2. **Broad research.** For flagship topics, discover at least 30 relevant video candidates where available. Then screen substantive material and deeply inspect complementary approaches. Metadata, transcript inspection, visual inspection, and listening are distinct evidence states.
3. **Competing routes.** Compare materially different explanations before selecting a coherent original route. The named creators are seeds, not the entire search boundary.
4. **Critical pilots.** Test the opening, hardest conceptual bridge, practical decision, and interactive or narrated delivery before expanding.
5. **Full understanding.** Cover what, why, when, where, mechanism, justification, applications, current uses, assumptions, limitations, diagnostics, mitigations, alternatives, best practices, and transfer.
6. **Depth with grounding.** Connect a shared conceptual core through child-level, teenage, undergraduate, graduate, PhD, and postdoc lenses. Actual readiness overrides age labels. Teach the learner to explain across audiences; six author-written summaries are insufficient.
7. **Interaction with a purpose.** Prediction, construction, comparison, diagnosis, and explanation should change the learner's reasoning. A moving slider alone is not evidence of learning.
8. **Production and review.** Keep exact speaker notes, visual cues, meaningful pauses, source provenance, mathematical checks, real runtime tests, and honest unresolved findings.

Quality takes priority over arbitrary authoring-time or slide-count limits. Long courses still need clear chapters, useful entry routes, and room to think. Repeated failed repairs trigger a change in strategy rather than indefinite cosmetic revision.

## Four distinct loops

| Loop | What changes |
|---|---|
| Authoring strategy | The overall explanatory route, informed by research and critical pilots |
| Explanation repair | A particular missing inference, misleading representation, or broken interaction |
| Learner practice selection | The next concept, case, representation, or support level |
| Learner step feedback | Help for the current attempt, followed by a suitable retry |

The [workflow CLI](skills/build-interactive-masterclass/references/harness.md) records declared dependencies, findings, revisions, and evidence receipts. It checks records; it does not determine truth, authenticate learning, or autonomously implement a tutor.

```bash
python skills/build-interactive-masterclass/scripts/test_harness.py
```

## Run the historical PCA course

Prerequisites: Python, [uv](https://docs.astral.sh/uv/), a network connection for first-time dependency installation, and Chrome or Edge for native notebook authoring. The historical launcher pins its Python packages and keeps a Deno lockfile.

From `outputs/pca-studio`, use two PowerShell terminals:

```powershell
# Editable notebook and native Studio view
.\Start-Lesson.ps1 -Edit
```

```powershell
# Built slide presentation
.\Start-Lesson.ps1
```

Open `http://localhost:2718/studio/lesson/` for the notebook and Studio, or `http://localhost:2719/lesson/` for the slides. Keep both terminals running. The outer slide page contains a **Back to notebook** link. A sandboxed in-app browser may block the notebook's service worker; use an external supported browser for authoring.

These are historical launch instructions, not a claim that a clean clone was retested on every operating system. The replacement course will have its own verified entry path and evidence.

## Repository layout and provenance

```text
skills/                         Current version 3.1 teaching skills
outputs/pca-studio/              Historical native Studio course and first-version recovery
outputs/tutor-retrospective*/    Versioned reports, snapshots, diffs, bundles, evidence
outputs/                        Other generated teaching assessments and previews
work/                           Generated source, research notes, reviews, and development records
archive-export-manifest.json     Exported-file hashes and explicit exclusions
```

Historical records preserve their original bytes, dates, local paths, failed checks, and qualifications. Some contain machine-specific paths or launch URLs. They document what happened; `skills/` is the maintained portable entrypoint. Do not treat an older snapshot as the current standard.

The archive includes generated artifacts, not copied account credentials, runtime caches, browser sessions, or downloaded third-party papers, notebooks, and workbook PDFs. Source URLs, notes, and inspection receipts are retained. Native marimo-studio and other dependencies remain separately installed packages with their own licenses. Linked creators and researchers do not endorse this project.

## Evidence and limitations

- Skill structure, workflow behavior, package hashes, source access, mathematical checks, and browser observations are recorded separately.
- The existing 31-video ledger is a discovery inventory. It is **not** a claim that 31 videos were watched or deeply analyzed.
- Creator research includes written guidance, selected transcript material, source notebooks, and static workbook inspection. Exact access is recorded in the notes.
- AI artifact review is not a human learning study. Unobserved learning, retention, performed narration, or audience outcomes remain unverified.
- A new build must generate current evidence. Historical passes do not automatically transfer to changed content or interfaces.

Publications should preserve these distinctions. The ambition is an exceptional explanation; there is no evidence-backed promise of a particular view count or improvement multiplier.
