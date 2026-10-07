"""Serve the native Studio view with a notebook link in its outer document.

The authored view stays in Studio's original sandbox. Top-level navigation
belongs in the outer page, so the link needs no iframe permission change.
"""
from pathlib import Path
from html import escape
import argparse
import re
import uvicorn
from marimo_studio import create_asgi_app


class NotebookNavigation:
    def __init__(self, app, editor_url):
        self.app = app
        self.link = (f'<a id="notebook-return" href="{escape(editor_url, quote=True)}">'
                     'Back to notebook &#8599;</a>').encode()
        self.css = ('#notebook-return{position:fixed;right:16px;top:9px;z-index:99999;'
                    'font:15px Segoe UI,Arial,sans-serif;color:#176859;'
                    'background:#fbfaf6;padding:9px 12px;text-decoration:none;'
                    'border-left:1px solid #d5ded7}')

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http' or scope.get('path') != '/lesson/':
            await self.app(scope, receive, send)
            return
        # The application can return compressed assets unchanged elsewhere.
        scope = {**scope, 'headers': [(k,v) for k,v in scope['headers'] if k.lower()!=b'accept-encoding']}
        start = None
        chunks = []
        async def capture(message):
            nonlocal start
            if message['type']=='http.response.start':
                start=message
            elif message['type']=='http.response.body':
                chunks.append(message.get('body',b''))
                if not message.get('more_body',False):
                    body=b''.join(chunks)
                    if start and start['status']==200 and b'marimo-studio-presentation' in body:
                        # Use the document's existing style nonce. Inline style
                        # attributes are blocked by Studio's strict CSP.
                        policy = next((v.decode() for k,v in start['headers']
                                       if k.lower()==b'content-security-policy'), '')
                        nonce = re.search(r"style-src\s+'nonce-([^']+)'", policy)
                        if nonce:
                            style = (f'<style nonce="{escape(nonce.group(1), quote=True)}">'
                                     f'{self.css}</style>').encode()
                            body=body.replace(b'</head>',style+b'</head>')
                        body=body.replace(b'</body>',self.link+b'</body>')
                    headers=[(k,v) for k,v in start['headers'] if k.lower()!=b'content-length']
                    await send({**start,'headers':headers+[(b'content-length',str(len(body)).encode())]})
                    await send({'type':'http.response.body','body':body})
            else:
                await send(message)
        await self.app(scope,receive,capture)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=2719)
    parser.add_argument('--editor-url',default='http://localhost:2718/studio/lesson/')
    args=parser.parse_args()
    notebook=Path(__file__).with_name('pca_lesson.py')
    app=NotebookNavigation(create_asgi_app(notebook),args.editor_url)
    uvicorn.run(app,host='127.0.0.1',port=args.port,log_level='warning')
