# Narration and video excellence protocol

Research and author-informed process audit, 6 October 2026. I previously contributed course code and the schema-2 guardrail; this is not an independent audit. No course or installed skill was changed for this report. The protocol below is a proposed production method, not a claim that a course has passed it.

## Ambition and evidence

Aim for a tutorial worth recommending: accurate, illuminating, coherent, visually precise, enjoyable to hear, and useful on a new problem. Treat a million views or top ratings as distribution ambitions, not acceptance criteria an author can guarantee. YouTube says high click-through rate and viewing duration can coexist with low impressions; traffic source, audience, and competing videos matter. Do not turn its published CTR ranges into a course target. [YouTube CTR FAQ](https://support.google.com/youtube/answer/7628154?hl=en)

Keep three ledgers separate: production quality; demonstrated learner reasoning; audience response. YouTube's retention report identifies first-30-second retention, dips, spikes, and top moments. A spike can reflect confusion and replay. A dip can reflect skipping or leaving. Compare similar-length material and relevant audience segments before forming a hypothesis. None measures conceptual transfer. [YouTube retention guidance](https://support.google.com/youtube/answer/9314415?hl=en)

YouTube's performance guidance describes long-term viewer satisfaction as an aim. Its dated 2021 engineering explanation discusses surveys alongside clicks, watch time, shares, and likes/dislikes, without a fixed recommendation formula. That is useful context, not a current algorithm specification or an available per-video learning score. [Current help](https://support.google.com/youtube/answer/141805?hl=en), [2021 engineering explanation](https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/)

Quality takes precedence over an invented duration or slide cap. A 100-plus-slide course is legitimate when its sequence earns the promised understanding. Every added scene still needs a job. A short matched-time experiment can compare a difficult bridge without limiting the finished course.

## From teaching route to performed explanation

**1. Define the full promise.** Specify the learner's starting model, central puzzle, useful capability, difficult inferences, applications, assumptions, failures, mitigations, alternatives, and transfer. Reserve the complete argument before writing an attractive opening. Plan chapter boundaries around questions resolved, not equal numbers of slides. Research admired explainers through actual representative visual and oral segments before attributing excellence to their animation or delivery; a transcript establishes neither.

**2. Write the spoken argument.** Draft exact narration alongside the scene, not a paragraph later labelled “speaker notes.” Use sentences a person can say naturally. State the question, show the revealing case, name what changed, justify the next move, and connect the result to the purpose. Define unfamiliar terms where needed. Remove repeated promises, exaggerated enthusiasm, “obviously,” and unexplained symbol reading. Direct instruction is appropriate when the learner lacks the knowledge needed to predict. Do not make constant guessing the price of progress.

**3. Make an event-cued storyboard.** For each meaningful change record: scene/cue ID; inference served; exact spoken words; visual state before and after; pointer target by stable object name; reveal or control action; intentional pause; expected reasoning; transition; and branch/re-entry conditions. Keep production directions separate from learner-facing speech. Estimate time initially, then replace it with observed rehearsal timing.

Example of a reusable cue structure:

| Cue | Spoken words | Visible action | Review question |
|---|---|---|---|
| product-pairs | “Multiply each term in the first bracket by each term in the second.” | Highlight four pairings one at a time; keep both brackets visible. | Can the viewer locate the source of every term? |
| combine | “These two products are equal, so together they give twice this product.” | Highlight the equal terms, then combine them; preserve the previous line. | Is the factor of two explained rather than announced? |

This is a proposed pattern, not an actual reviewed scene.

**4. Speak mathematics as reasoning.** Name what an expression measures before reading its symbols. Identify the objects, units, dimensions, assumptions, operation, and reason the operation helps. Distinguish an example from an identity, an approximation from equality, and a necessary condition from a sufficient one. Say “sum over observations” when that meaning is clearer than reciting notation, while pointing to the exact index. Explain why a denominator, constraint, sign, or cross term appears. Pause after a new definition or inferential step, not mechanically after every equation. Use consistent names across audio, formulas, diagrams, and feedback.

**5. Rehearse an inexpensive but complete animatic.** Combine rough visuals with the intended spoken text before expensive illustration work. Actually read aloud or generate and listen to the intended voice. Record stumbling, ambiguous references, pronunciation, breath, emphasis, dead time, premature reveals, and moments when the listener must read while the explanation moves on. Rehearse the opening, hardest bridge, and transfer first; then the whole route. Report measured duration separately from estimated duration. Do not prescribe a universal words-per-minute law. A technical inference and a familiar recap need different processing time.

**6. Produce coordinated illustrations and delivery.** Use diagrams whose geometry, labels, values, and motion are correct. Make the important relation visible before decorating it. Preserve reference states through transformations. Direct the cursor deliberately and hold its target long enough to identify it; avoid idle wandering. Make narration refer to named objects, not only “this” or “over here.” Check the intended screen sizes, contrast, equation legibility, captions, audio clarity, and whether a presenter overlay obscures needed information.

Mayer and Anderson's two experiments on narrated explanations of mechanical systems found an advantage for concurrent words and animation on problem-solving transfer over the tested alternatives. This supports testing word–picture coordination; it does not prove that every animation, speaking pace, or course format teaches better. [Primary study, 1992](https://doi.org/10.1037/0022-0663.84.4.444)

W3C recommends planning accessibility during scripting and storyboarding, clear speech, suitable pauses, low competing noise, readable text, and descriptions of relevant visual information. Integrate such description where practical; provide appropriate captions, transcript, and alternatives. These recommendations do not constitute a completed accessibility audit. [W3C audio/video content](https://www.w3.org/WAI/media/av/av-content/), [integrated description technique](https://www.w3.org/WAI/WCAG22/Techniques/general/G226)

## Review the experience through different channels

**Silent-picture test:** inspect the rendered sequence without audio. Can a reviewer track the objects, changes, comparisons, and visual question? Where does the diagram contradict or hide the intended relation? This tests visual support; it need not make every argument independently recoverable without narration.

**Audio-only test:** listen without seeing the display. Does the reasoning have a clear purpose and sequence? Are referents, quantities, and transitions identifiable? Flag essential spatial information that needs description or an accessible alternative. Do not “fix” every visual dependence by burdening the ordinary soundtrack with unreadable coordinate lists.

**Combined timed test:** play the actual audio and visual sequence at its intended pace. Inspect correspondence at difficult cues, overload, pronunciation, caption accuracy, and time to inspect or reason. A source-code read or word count is not this test. If audio tools are unavailable, label oral review unperformed.

**Cold speaker handoff:** give another presenter the notes and operational cues. Can they deliver the intended argument and operate the illustration without asking the author what a cue means? This tests whether notes are publication-ready rather than reminders intelligible only to their writer.

**Novice reasoning test:** ask an uncoached learner to predict, explain a critical step, reject a plausible wrong rule, and handle a new case. Preserve their reasoning and assistance. A knowledgeable AI's correct answer is not novice learning evidence. AI review should cite the learner-visible warrant it used. Delayed retrieval and transfer require actual later observations.

Review findings identify the cue, observed problem, learner consequence, proposed causal change, and recheck. Repair the affected obligation; replay adjoining transitions when timing or sequence changes. Also conduct a complete route review. Do not substitute a beauty score, number of reviewers, or completed checklist for observations.

## Two delivery paths, one conceptual route

A linear video needs an authored demonstration path. The narrator chooses inputs, shows consequential alternatives and failures, offers pause-and-predict moments, and reveals justified feedback. It cannot claim to respond to a viewer's answer. Chapters and optional companion exercises support different readiness levels without making the main argument incoherent.

An interactive lesson needs state-aware narration and notes. Describe the actual selected case and values; specify when to wait, how to respond to an error, and how to return from a question. Student interruption must stop stale speech or pointing. Reset and back navigation must restore meaningful state. Avoid pre-recorded praise that claims a correct response regardless of the learner's action. Test these branches separately from the linear demonstration. Exporting notebook slides alone does not establish video-production quality.

Deliver an editable script, event-cued speaker notes, storyboard, original or licensed illustration assets, source/credit record, intended delivery path, and review evidence. Include actual audio/video, corrected captions, and transcript when commissioned and produced. A script-only deliverable must not claim that oration or synchronization was tested. Keep “reviewed production candidate,” “human learning observed,” and “published audience response” distinct.

After authorized publication, map retention observations back to scene IDs and test explanations for dips or replay. Do not delete a needed proof merely to improve viewing metrics. YouTube's native title/thumbnail tests compare concurrent variants using watch-time share and can be inconclusive; use them for honest packaging, not as proof of learning. [YouTube A/B testing](https://support.google.com/youtube/answer/16391400?hl=en)

## Precise skill and guardrail amendments

Audit snapshot is concurrent with the coordinator's edits; recommendations below distinguish remaining text from changes already visible.

- **Canonical SKILL.md, inner-loop paragraph; harness.md paragraphs 9–11:** replace the general instruction to declare bounded research/pilot/repair “action limits” with explicit user constraints and quality obligations. Working allocations are revisable planning aids when the user prioritizes quality. Do not stop merely because an internally invented allocation expired. Keep stopping unchanged reviews and preserving honest incomplete status.
- **Two unsuccessful repairs:** retain strategy reopening, failure history, changed causal hypothesis, and a fresh pilot. This is not a total work cap: the existing CLI permits continued repairs after that transition. Clarify this in SKILL.md and replace “Repair cap reached” in harness.py lines 217/299 with “Strategy review required before repeating this repair.” Do not weaken the safeguard merely to permit endless cosmetic iterations. The hard-coded threshold is an operational checkpoint, not an empirical learning law.
- **Outer-loop route count; harness.md paragraph 9:** say “begin with two or more materially different routes; expand when unresolved decisions warrant it,” not “two normally suffice.” The concurrently revised research-debate.md already makes this distinction, permits 100-plus slides, and treats 8–12 deep candidates as a starting allocation rather than a ceiling. Preserve that correction and remove contradictory wording elsewhere.
- **Review/delivery and review.md:** add spoken-script, cue synchronization, actual aloud/listening, silent-picture, audio-only, and cold-presenter evidence. Extend the learner-facing prose audit to spoken narration; exclude internal production cues. Do not impose a universal speech-rate target or claim a full STE audit from short sentences.
- **Minimal implementation:** maintain one canonical narration reference and link it from the alias skill. Register script, storyboard, audio, rendered sequence, and shared inputs in existing inference/review nodes so changes invalidate affected evidence. Existing artifact, visual, interaction, and teaching-review claims suffice initially; receipt scenarios can name the actual oral test. Do not build a second media workflow engine or fabricate receipts for tests not performed.

## Access limits

Official YouTube and W3C page text was inspected on 6 October 2026. The 2021 engineering article is explicitly historical. The Mayer–Anderson primary PDF was accessible through the author's ResearchGate copy; relevant experimental and discussion text was inspected. A separate Mayer–Chandler PDF failed to open; its indexed abstract is not used as substantive evidence here. No exemplar video was watched or listened to during this task, no learner study ran, and no course oration was assessed. The detailed production procedure is a reasoned proposal informed by these sources, not a validated universal formula.
