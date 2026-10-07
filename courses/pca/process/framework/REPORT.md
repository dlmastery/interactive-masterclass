# Native Studio framework investigation

Date: 2026-10-07. Scope: read-only inspection of installed packages, upstream bundled starter, and historical PCA source; one isolated synthetic transport probe. No course source was changed, no service was started or stopped, and no package was downloaded or installed. This report does not establish browser acceptance.

After this investigation, the parent authorized implementation of the new notebook runtime. See [RUNTIME.md](RUNTIME.md) for the files, exact projection schema, launch instructions, and completed numerical/source checks. The read-only statement above describes the investigation phase, not that later implementation.

## Decision

Use **marimo-studio 0.2.3's native `marimo-studio/react:reveal` starter** for a new course under `courses/pca/`. Keep Python computation and native data controls in its notebook. Mount native controls with `<marimo-cell>`, consume computed results with explicit `mo-value` hosts and the supplied update hook, and use Reveal `Slide`/`Fragment` for presentation and derivation steps. Use the native Studio editor shell as the primary authoring/learning route so the notebook remains available. Prove that actual shell navigation in the pilot before choosing a separate production server.

Preserve `outputs/pca-studio/` as history. Do not copy its claims, unused components, generated artifacts, or hardcoded ports into the new course. Reuse small verified mathematical routines only with fresh tests and explanation review.

## Installed evidence and exact locations

For compact references below:

- `PKG = C:/Users/abhir/AppData/Local/uv/cache/archive-v0/hddNGIiaopNekzO3V-OGi/marimo_studio`
- `SKILL = C:/Users/abhir/AppData/Local/uv/cache/archive-v0/hddNGIiaopNekzO3V-OGi/marimo_studio-0.2.3.agent-plugin/skills/marimo-studio`
- `ENV = C:/Users/abhir/AppData/Local/uv/cache/archive-v0/Uh5Wq7_loXbaJx6gGVzsv`
- `NPM = C:/Users/abhir/AppData/Local/deno/npm/registry.npmjs.org`
- Repository: `C:/Users/abhir/Documents/Codex/2026-10-03/exp/interactive-masterclass`

These cache paths are local investigation evidence, **not portable launch dependencies**.

Inspected repository `AGENTS.md`, `skills/build-interactive-masterclass/SKILL.md`, its `references/marimo-studio.md`, and historical `outputs/pca-studio/v/lesson/AGENTS.md`. Read installed Studio skill and its projections/delivery references. Read the original bundled Reveal starter's `AGENTS.md`, `src/App.tsx`, types, hook, and provider registration. These bundled files are upstream example source, not this project's historical adaptation. No separate remote showcase was inspected.

Executed:

```powershell
& "$ENV/Scripts/python.exe" -c 'import importlib.metadata as m; import sys; print(sys.executable); print({n:m.version(n) for n in ["marimo-studio","marimo","numpy","deno"]})'
& "$ENV/Scripts/marimo-studio.exe" starters --json
```

Result: Python environment reports `marimo-studio=0.2.3`, `marimo=0.25.0`, `numpy=2.5.3`, `deno=2.9.7`. Starter catalog returns `marimo-studio/react:reveal`, title `Reveal.js slides`, `available=true`, Deno version `2.9.7`. Studio metadata independently pins marimo 0.25.0 and requires Python >=3.10,<3.15. **NumPy 2.5.3 requires Python >=3.12**, so the new course must declare >=3.12,<3.15 and its launcher selects Python 3.12. The historical notebook's >=3.10 declaration is too broad for its NumPy pin.

A different cached environment (`archive-v0/mJfnJwpcF76hST7BoZqSr`) had Studio/marimo/numpy but **no Deno extra**; its starter catalog correctly returned `available=false`. Do not infer build availability from successful `import marimo_studio` alone. No installation was necessary because the complete cached environment exists.

Historical frontend manifests pin `@revealjs/react=0.2.1`, `reveal.js=6.0.1`, React 19.2.4, KaTeX 0.16.22. Their packages are present in the Deno cache. The historical notebook pins Studio 0.2.3 and numpy 2.5.3.

## Supported lifecycle and portable commands

The following commands are **source-confirmed recommendations, not a new clean-start test**. Execute from the new course directory after its notebook exists. Use repository-relative paths and inline notebook dependencies; never bake the investigated cache path into launch scripts.

```powershell
# First-time native view creation (mutates only the new course).
uvx --python 3.12 --from 'marimo-studio[deno]==0.2.3' marimo-studio view create lesson --target pca.py --starter 'marimo-studio/react:reveal'

# Notebook authoring and native Studio shell.
uvx --python 3.12 --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' marimo edit pca.py --no-sandbox --watch --host 127.0.0.1 --port <free-port>

# Build the exact production artifact.
uvx --python 3.12 --from 'marimo-studio[deno]==0.2.3' marimo-studio view build lesson --target pca.py --profile production

# Optional separate run-mode presentation.
uvx --python 3.12 --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' marimo run pca.py --no-sandbox --host 127.0.0.1 --port <different-free-port>
```

`--no-sandbox` here means marimo's Python environment selection, as in the historical launcher; it does not weaken Studio's browser iframe sandbox. Alternative supported environment policy: declare all dependencies in the PEP 723 header and use `--sandbox`. Select one policy and test it from a clean shell. Keep `--watch` for external notebook edits. Add `--no-token` only if local pairing is deliberately needed; the packaged skill uses it for discoverability. Do not copy authentication/session URLs into public records.

Python authoring API is `marimo_studio.authoring.open_workspace(notebook_path)`, then `await workspace.starters()`, `await workspace.create_view("lesson", starter="marimo-studio/react:reveal")`, `workspace.view("lesson")`, and `await view.build(profile="production")`. In notebook code mode, use `marimo_studio.agent.current_workspace()` and reacquire handles per execution. `view.show()` is a live Studio operation; finish its code-mode execution before browser checks. `view.preview_url(runtime="server", exact=True)` is the documented exact production-preview path; terminal lookup additionally needs the running server URL.

`marimo_studio.create_asgi_app(notebook)` is public, documented as a run-mode Marimo app (`PKG/__init__.py:29`). It remains an option for an outer navigation wrapper, not a requirement for a native deck. `view build` packages browser code; it does not execute changed notebook Python. A prior successful artifact can survive a failed build. Check revision and freshness as well as browser appearance.

Evidence: `SKILL/SKILL.md`; `SKILL/references/delivery.md`; `PKG/_cli/commands/view_catalog.py:45`; `PKG/_cli/commands/view_delivery.py:100`; `PKG/_authoring/workspace_api.py:166`; `PKG/_authoring/view_api.py:133`.

## Interaction contract

| Intended action | Supported mechanism | Honest learner claim |
|---|---|---|
| Change observation or parameter and recompute covariance/eigenvectors | `mo.ui` control in notebook; display its named cell with `<marimo-cell name="data_controls" />`; downstream cells depend on `.value` | This change recomputes notebook results in the active runtime |
| Read the current computed model in React | Explicit `<span ref={hostRef} hidden mo-value="pca_case" />` plus bundled `useMarimoValue` | The diagram displays notebook results |
| Drag angle smoothly over finite precomputed cases | Browser state indexes Python-computed frames | This control selects a precomputed angle/frame |
| Select a frame too large to project as one combined table | Dynamic `mo-value` selector on `data-marimo-allow="*"` host; compact index plus keyed Python values | This selects a computed notebook result; it is not arbitrary Python execution |
| Advance derivation | Reveal `Fragment`, native next/back controls | Reveal one justified step at a time |

The installed projections reference explicitly says views change notebook state through **native marimo controls** and keep other selection state in the browser. It documents no general custom-JavaScript-to-Python setter. Do not construct a private RPC bridge or promise Python execution on every custom drag. A meaningful pilot should project a native slider, change it, and verify a downstream Python-produced number and diagram both update.

The supplied React hook reads `host.marimoValue`, subscribes to `marimo-value-updated` and `marimo-value-error`, and synchronizes existing host state on mount. Preserve explicit authored hosts for provider authorization. Link each custom figure to all its inputs through host IDs and `data-marimo-lens-inputs`; retain rendering source/label metadata. Do not modify native output internals.

Historical source has a valid example of the intended ownership: `pca_lesson.py:147-159` defines native observation-D sliders and computes `sandbox_lab`; `PcaScenes.tsx:1817` projects `masterclass_controls`; `PcaCourse.tsx:130` projects `sandbox_lab`. This is source evidence, not a fresh test that the old browser session reflects it.

Dynamic selectors are supported by Python runtime and Browser/WASM runtime. Prepared export requires finite authored targets; its state file must enumerate available control states. A browser-only selection among already projected frames is distinct from Studio's Prepared export runtime.

## Payload limits: confirmed aggregate constraint

`PKG/_projections/runtime_records.py:9` sets `MAX_RUNTIME_VALUE_BYTES = 1_000_000`. The packaged projections reference states the per-value bound. Server implementation additionally enforces a combined response bound:

- `PKG/_compat/kernel_values/selectors.py`, `_read_values`: `max_response_bytes` defaults to `DEFAULT_MAX_VALUE_BYTES`.
- It rejects a selector when the sum of encoded values exceeds that bound (line 138) and checks serialized UTF-8 response size including its envelope (line 196).
- `PKG/_compat/kernel_values/kernel.py:475` clamps requested per-value size and calls `_read_values` without raising its response limit.

Executed an isolated synthetic probe using the installed `_read_values` (an internal API used **only as investigation evidence**, not proposed course code): two strings of 600,000 characters each, each independently below the limit. Result:

```json
{"limit":1000000,"retained":["a"],"errors":{"b":{"code":"response-too-large","message":"The value response exceeds the aggregate byte limit."}}}
```

Keep ample headroom. Prefer a compact current dataset plus a small angle table, shared notation/course content, and one selected scenario. Do not project duplicate point clouds and full repeated frames for every slide. Measure encoded payload under all supported native-control states; the historical 940,547-byte claim was not remeasured here. A per-value size check alone is insufficient.

## Slides, notes, and keyboard behavior

The original bundled starter uses `Deck`, `Slide`, `deckRef`, `reveal.js/reveal.css`, a `marimo-studio:idle` listener that calls `deck.layout()`, and `keyboardCondition` that avoids intercepting events from `marimo-cell`/`marimo-output`. Preserve these behaviors. Extend keyboard exclusion for custom inputs, buttons, textareas, selects, and open dialogs.

The installed starter explicitly requires `scrollActivationWidth: 0`: Reveal's automatic narrow scroll mode reads `sessionStorage`, unavailable in Studio's opaque-origin frame. Use neutral `div` wrappers inside a slide; add nested `section` only for an intentional Reveal vertical stack.

`NPM/@revealjs/react/0.2.1/README.md` and `dist/components/slide.d.ts` support `Slide notes`, `Fragment`, `Stack`, plugins at initial mount, and `Deck.config`. The README says config is **shallow-compared**, so an inline object with unchanged primitive properties is not itself proof of reinitialization. Stable callback values and a stable config object remain a sensible precaution; do not repeat the historical blanket claim that any new config identity resets the deck. Plugins are initialization-only.

Reliable notes design to pilot: store narration with course records, pass it as `Slide notes={...}` or `<aside className="notes">`, and provide inline notes via Reveal's `showNotes` or a readable course notes panel. `NPM/reveal.js/6.0.1/js/controllers/notes.js` directly implements `showNotes`, `data-notes`, and `aside.notes`. Readable notebook narration provides a second access route.

Do not count popup presenter notes as verified. The bundled `dist/plugin/notes.mjs` checks `window.opener.location.origin` and same-origin events. Studio uses an opaque-origin frame. This is a concrete compatibility risk from source, **not a tested failure**. Prefer inline notes until the real browser probe proves otherwise. No framework patch or sandbox relaxation is recommended.

## Safe navigation and notebook return

`PKG/_server/presentation/isolation.py:37-40` sets the presentation sandbox to:

```text
allow-downloads allow-forms allow-modals allow-pointer-lock allow-popups allow-scripts
```

There is no `allow-same-origin`, `allow-top-navigation`, or `allow-popups-to-escape-sandbox`. A target-blank link from inside the slide frame should not be assumed to open an unrestricted notebook editor. The same file documents a trusted parent shell owning allowed view navigation, public history, and readiness.

Preferred path: launch `marimo edit`, keep the native Studio shell open, and use its notebook surface alongside the view. Source includes a retained native editor iframe and native-editor route (`PKG/_server/studio/document.py`; `PKG/_delivery/urls.py:67-73`). `studio_url` is `/studio/<view>/`; `editor_url` builds `/_studio/editor/` with notebook/session binding parameters. Use the shell-generated actual route; do not manufacture binding tokens or assume an old localhost link identifies the new notebook.

If a dedicated full-screen run-mode page is needed, keep its notebook-return link in a **trusted outer document**, with an explicit editor URL provided by the launcher. Historical `serve_lesson.py` demonstrates this composition around public `create_asgi_app`; it preserves the authored iframe and uses the response's CSP nonce. That exact HTML-rewrite wrapper needs new integration verification and configurable routes/ports before reuse. A separate run-mode process has its own runtime/session; returning to an editor does not by itself prove cross-process state continuity. Prefer one editor shell for the pilot and explicitly test state behavior before promising persistence.

## Minimal new course design

```text
courses/pca/
  pca.py                    # PEP 723 pins, model, native inputs, explanation
  Start-Course.ps1          # relative paths, configurable unused port
  README.md                 # actual tested entry/return/refresh instructions
  v/lesson/
    view.toml               # provider = "marimo-studio/react"
    deno.json + deno.lock    # frozen exact frontend dependencies
    AGENTS.md
    src/App.tsx             # Deck, slides, native projections, fragments
    src/Scenes.tsx          # focused diagram components
    src/style.css
    src/lib/use-marimo-value.ts
    src/marimo-studio.d.ts
  process/                  # research, plans, framework and verification evidence
```

Use a new notebook and native starter rather than copying the complete historical view tree. Keep notes and scene content in one authored record structure to avoid mismatched narration. Project only notebook-derived values/claims. Browser layout/labels and presentation interaction may remain in TSX. Keep the editable notebook mathematically readable without slides. Keep archived TSX out of the new view source root; the provider declares analysis suffixes for JS/JSX/MJS/TS/TSX and the historical project reports unused-source projection scanning. This investigation did not separately execute a scan probe.

## Required next pilot, before mass authoring

1. Build a new native starter and inspect the exact published revision and freshness.
2. Show a small Python-owned point set, native parameter control, projected covariance/eigenvalue result, and correctly scaled geometry. Change the native control in the actual browser and verify all outputs agree with a recomputation.
3. Use a browser angle selector over clearly identified precomputed frames, and verify reset and revisit state.
4. Advance/back through one derivation with Reveal fragments; check arrow keys while an input has focus, and check controls by pointer.
5. Toggle readable notes. Verify the full note text at the actual viewport size.
6. Return to the editable notebook through the actual native shell or trusted outer link; verify the intended file and demonstrate an editable cell. Test return to slides and state behavior.
7. Repeat at realistic wide/narrow host sizes; inspect legibility, scrolling, and formula/diagram/value agreement. Do not equate a successful build with this acceptance.
8. Record clean-start commands, required process count, actual routes, payload measurements, revision, and any offline/export limitations. A live server test does not validate a Prepared or WASM export.

Until this pilot runs, framework support is established by installed source/catalog evidence and a bounded transport probe; live course interaction, browser notes, navigation, launch portability, and human learning remain unverified.
