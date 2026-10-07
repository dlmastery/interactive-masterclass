"""Check the narrow ASGI navigation composition without starting a server."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from serve_lesson import NotebookNavigation, notebook_url_from_file


class AuthenticatedNotebookUrl(unittest.TestCase):
    def convert(self, value, expected="http://localhost:2728/studio/lesson/"):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "editor-link.txt"
            path.write_text(value, encoding="utf-8-sig")
            return notebook_url_from_file(path, expected)

    def test_generated_root_url_becomes_studio_return(self):
        self.assertEqual(
            self.convert("http://localhost:2728?access_token=synthetic-test-token\n"),
            "http://localhost:2728/studio/lesson/?access_token=synthetic-test-token",
        )

    def test_custom_port_and_query_encoding(self):
        self.assertEqual(
            self.convert("http://localhost:2738/?access_token=fake%2Bvalue%26only",
                         "http://localhost:2738/studio/lesson/"),
            "http://localhost:2738/studio/lesson/?access_token=fake%2Bvalue%26only",
        )

    def test_other_origins_credentials_and_invalid_tokens_are_rejected(self):
        for value in [
            "http://localhost:2729?access_token=fake",
            "http://example.test:2728?access_token=fake",
            "http://user:password@localhost:2728?access_token=fake",
            "http://localhost:2728?access_token=",
            "http://localhost:2728?access_token=fake&access_token=other",
            "http://localhost:2728/auth/login?access_token=fake",
            "http://localhost:2728?access_token=fake#fragment",
            "http://localhost:2728?access_token=fake\nsecond-line",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.convert(value)


class NotebookReturn(unittest.IsolatedAsyncioTestCase):
    async def render(self, path="/lesson/", status=200, encoding=None):
        original = b'<html><head></head><body><iframe id="marimo-studio-presentation" sandbox="allow-scripts"></iframe></body></html>'
        policy = b"default-src 'self'; style-src 'nonce-test123'; script-src 'self'"
        headers = [(b"content-type", b"text/html; charset=utf-8"),
                   (b"content-security-policy", policy),
                   (b"content-length", str(len(original)).encode()), (b"etag", b'"old"')]
        if encoding:
            headers.append((b"content-encoding", encoding))
        seen = []

        async def app(scope, receive, send):
            seen.append(scope)
            await send({"type": "http.response.start", "status": status, "headers": headers})
            await send({"type": "http.response.body", "body": original[:50], "more_body": True})
            await send({"type": "http.response.body", "body": original[50:]})

        sent = []

        async def send(message):
            sent.append(message)

        await NotebookNavigation(app, "http://localhost:2728/studio/lesson/")(
            {"type": "http", "path": path, "headers": [(b"accept-encoding", b"gzip")]}, None, send,
        )
        return original, policy, sent, seen

    async def test_link_uses_existing_nonce_and_preserves_sandbox(self):
        original, policy, sent, seen = await self.render()
        body = sent[1]["body"]
        headers = dict(sent[0]["headers"])
        self.assertIn(b'Back to editable notebook', body)
        self.assertIn(b'href="http://localhost:2728/studio/lesson/"', body)
        self.assertIn(b'<style nonce="test123">', body)
        self.assertIn(b'sandbox="allow-scripts"', body)
        self.assertEqual(headers[b"content-security-policy"], policy)
        self.assertEqual(int(headers[b"content-length"]), len(body))
        self.assertNotIn(b"etag", headers)
        self.assertEqual(seen[0]["headers"], [])

    async def test_default_route_gets_the_same_return_path(self):
        _, _, sent, _ = await self.render(path="/")
        self.assertIn(b'Back to editable notebook', sent[1]["body"])

    async def test_asset_response_is_unchanged(self):
        original, _, sent, seen = await self.render(path="/_studio/assets/test.html")
        self.assertEqual(b"".join(item.get("body", b"") for item in sent), original)
        self.assertEqual(seen[0]["headers"], [(b"accept-encoding", b"gzip")])

    async def test_errors_and_unexpected_compression_are_unchanged(self):
        for options in [{"status": 500}, {"encoding": b"gzip"}]:
            original, _, sent, _ = await self.render(**options)
            self.assertEqual(sent[1]["body"], original)
            self.assertIn(b"etag", dict(sent[0]["headers"]))


if __name__ == "__main__":
    unittest.main()
