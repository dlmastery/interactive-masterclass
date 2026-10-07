# Native editor connection diagnosis

Read-only HTTP and installed-package inspection, 6 October 2026. No browser actions or configuration/security changes.

## Observed

- Fresh `http://localhost:2718/studio/lesson/` returns 200.
- Its exact generated `iframe#marimo-studio-editor` URL also returns 200 with the native marimo editor HTML. The same holds with `127.0.0.1` instead of `localhost`.
- Both responses have exactly one framing CSP: `frame-ancestors 'self'`. Neither sends `X-Frame-Options`, an additional CSP, or a CSP meta tag. The generated iframe is same-origin and has no sandbox attribute. Referenced scripts are also same-origin.
- No login redirect appears. The bare `/` route redirects to `/studio/lesson/`; it is not a separate native notebook entry point.
- Query **names only** and selected safe response headers are recorded in `work/editor-http-diagnosis.jsonl`. Capability values were neither printed nor saved.

## Browser evidence supplied by the parent

The native editor also remained blank when its fresh generated URL was opened at the top level of the in-app browser. The browser console reported a `SecurityError` when reading `navigator.serviceWorker`: the context is sandboxed and lacks `allow-same-origin`. This identifies the in-app browser sandbox as the authoring failure. It is not evidence of a failed Studio server or an invalid fresh capability.

The parent subsequently opened Studio in Chrome and verified that the actual notebook, preview, and code-mode session loaded there.

## Meaning

Fresh routing, notebook resolution, and binding capability validation succeed at the HTTP level. Combined with the browser console and successful Chrome session, the evidence identifies an in-app browser authoring limitation.

Installed Studio code confirms the native editor mount is `/_marimo-studio/editor/`. The outer document generates a session-bound editor URL. `editor_bridge.py` rejects invalid/absent required bindings with HTTP 403; that is not the response observed for freshly generated URLs. `headers.py` deliberately applies same-origin framing to editor documents.

## Working authoring path

Open `http://localhost:2718/studio/lesson/` in Chrome for the verified native authoring workflow. Edge is also an ordinary external browser option, but it was not tested in this investigation. Use Studio's **Show Notebook** checkbox or **Visible surface** control, according to the window layout. The slideshow remains available at `http://localhost:2719/lesson/`.

Do not weaken Studio CSP or the in-app browser sandbox. Do not publish capability parameters or hand-author the internal editor URL. Another reinstall or restart is not justified by this evidence.

No persisted current-server log file was present in the workspace. Browser evidence and the successful external Chrome check were supplied by the parent agent; this subagent performed no browser actions.
