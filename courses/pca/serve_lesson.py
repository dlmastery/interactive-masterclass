"""Serve the native Studio view with an outer-page return to its notebook.

The view remains inside Studio's original browser sandbox. The return link
belongs to the trusted outer document. Run the editor separately; run-mode
and editor sessions do not share live control state.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def notebook_url_from_file(path: str | Path, expected_editor_url: str) -> str:
    """Read a local generated login URL without logging its credentials.

    Only an exact local editor origin is accepted. Keep its access token while
    directing the user to this course's native Studio workspace.
    """
    raw = Path(path).read_text(encoding="utf-8-sig").strip()
    if len(raw) > 8192 or any(char.isspace() for char in raw):
        raise ValueError("The editor URL file must contain one generated URL.")
    parsed, expected = urlparse(raw), urlparse(expected_editor_url)

    def origin(value):
        if (value.scheme not in {"http", "https"}
                or value.hostname not in {"localhost", "127.0.0.1", "::1"}
                or value.username is not None or value.password is not None):
            raise ValueError("The editor URL must use the requested local HTTP(S) origin.")
        return value.scheme, value.hostname, value.port or (443 if value.scheme == "https" else 80)

    if origin(parsed) != origin(expected):
        raise ValueError("The editor URL file does not match the requested editor origin.")
    if parsed.path not in {"", "/", "/studio/lesson", "/studio/lesson/"} or parsed.fragment:
        raise ValueError("The editor URL file does not identify the course editor.")
    tokens = [value for key, value in parse_qsl(parsed.query) if key == "access_token"]
    if len(tokens) != 1 or not tokens[0]:
        raise ValueError("The generated editor URL must contain one access token.")
    return urlunparse((expected.scheme, expected.netloc, "/studio/lesson/", "",
                       urlencode({"access_token": tokens[0]}), ""))


class NotebookNavigation:
    """Add a notebook link without changing Studio's iframe or CSP policy."""

    def __init__(self, app, editor_url: str):
        parsed = urlparse(editor_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("The editor URL must be an absolute HTTP(S) URL.")
        self.app = app
        self.link = (
            '<a id="notebook-return" href="'
            + escape(editor_url, quote=True)
            + '">Back to editable notebook</a>'
        ).encode("utf-8")
        self.css = (
            "#notebook-return{position:fixed;right:12px;top:8px;z-index:99999;"
            "font:600 14px/1.3 system-ui,sans-serif;color:#143b32;"
            "background:#fffef7;padding:9px 12px;border:1px solid #8ba497;"
            "border-radius:6px;text-decoration:none;max-width:70vw}"
            "#notebook-return:focus-visible{outline:3px solid #176859;outline-offset:2px}"
            "@media(max-width:600px){#notebook-return{font-size:12px;padding:6px 8px}}"
        )

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path") not in {"/", "/lesson/", "/lesson"}:
            await self.app(scope, receive, send)
            return

        # Request the outer page uncompressed before adding its link. All asset
        # responses and the actual authored iframe are passed through untouched.
        scope = {
            **scope,
            "headers": [(key, value) for key, value in scope.get("headers", [])
                        if key.lower() != b"accept-encoding"],
        }
        start = None
        chunks = []

        async def capture(message):
            nonlocal start
            if message["type"] == "http.response.start":
                start = message
                return
            if message["type"] != "http.response.body":
                await send(message)
                return
            chunks.append(message.get("body", b""))
            if message.get("more_body", False):
                return
            if start is None:
                raise RuntimeError("ASGI response body arrived before its headers.")
            body = b"".join(chunks)
            headers = list(start.get("headers", []))
            header_map = {key.lower(): value for key, value in headers}
            is_html = b"text/html" in header_map.get(b"content-type", b"")
            is_plain = header_map.get(b"content-encoding", b"identity") == b"identity"
            modified = False
            if (start["status"] == 200 and is_html and is_plain
                    and b"marimo-studio-presentation" in body
                    and b'id="notebook-return"' not in body):
                policy = header_map.get(b"content-security-policy", b"").decode("utf-8")
                nonce = re.search(r"style-src\s+'nonce-([^']+)'", policy)
                if nonce:
                    style = (
                        '<style nonce="' + escape(nonce.group(1), quote=True)
                        + '">' + self.css + '</style>'
                    ).encode("utf-8")
                    body = body.replace(b"</head>", style + b"</head>", 1)
                if b"</body>" in body:
                    body = body.replace(b"</body>", self.link + b"</body>", 1)
                    modified = True
            if modified:
                headers = [(key, value) for key, value in headers
                           if key.lower() not in {b"content-length", b"etag", b"content-md5"}]
                headers.append((b"content-length", str(len(body)).encode("ascii")))
            await send({**start, "headers": headers})
            await send({"type": "http.response.body", "body": body})

        await self.app(scope, receive, capture)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=2729)
    parser.add_argument("--editor-url", default="http://localhost:2728/studio/lesson/")
    parser.add_argument("--editor-url-file", type=Path,
                        help="Ignored local file containing the generated authenticated editor URL.")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    editor_url = args.editor_url
    if args.editor_url_file:
        try:
            editor_url = notebook_url_from_file(args.editor_url_file, args.editor_url)
        except (OSError, ValueError):
            # Do not include the URL, file content, or parser exception: any may
            # contain an authentication credential.
            parser.error("Unable to read a valid authenticated URL for the requested local editor.")

    import uvicorn
    from marimo_studio import create_asgi_app

    notebook = Path(__file__).with_name("pca_lesson.py")
    app = NotebookNavigation(create_asgi_app(notebook), editor_url)
    print(f"Slides: http://localhost:{args.port}/lesson/")
    print("Editable notebook: use the authenticated outer-page return link.")
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
