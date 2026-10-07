from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlsplit, urljoin, parse_qs, urlunsplit
from html.parser import HTMLParser
import html, json

class Iframes(HTMLParser):
    def __init__(self):
        super().__init__(); self.frames=[]; self.links=[]; self.meta=[]; self.scripts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='iframe': self.frames.append(a)
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='meta' and a.get('http-equiv','').lower()=='content-security-policy': self.meta.append(a.get('content',''))
        if tag=='script' and a.get('src'): self.scripts.append(a['src'])

def redact_url(url):
    parts=urlsplit(url)
    keys=list(parse_qs(parts.query))
    return urlunsplit((parts.scheme,parts.netloc,parts.path,'[query keys: '+','.join(keys)+']' if keys else '', ''))

opener=build_opener(HTTPCookieProcessor())
def inspect(url):
    try:
        with opener.open(url,timeout=15) as r:
            body=r.read().decode('utf-8',errors='replace')
            headers=[(k,(redact_url(v) if k.lower()=='location' else v)) for k,v in r.headers.items() if k.lower() in {'content-security-policy','x-frame-options','location','content-type','server','referrer-policy'}]
            parser=Iframes(); parser.feed(body)
            print(json.dumps({'request':redact_url(url),'final':redact_url(r.url),'status':r.status,'headers':headers,
                'body_markers':{x:x in body for x in ['marimo-studio-editor','marimo-studio-presentation','login','Sign in','<marimo','marimo-code','marimo-filename']},
                'frames':[{'id':f.get('id'),'src':redact_url(urljoin(r.url,f.get('src',''))),'sandbox':f.get('sandbox')} for f in parser.frames],
                'meta_csp':parser.meta,
                'script_origins':sorted(set(urlsplit(urljoin(r.url,s)).netloc for s in parser.scripts))},indent=2))
            return body,parser,r.url
    except Exception as e:
        print(json.dumps({'request':redact_url(url),'error_type':type(e).__name__,'error':str(e).split('?')[0]},indent=2))
        return '',Iframes(),url

for host in ['localhost','127.0.0.1']:
    body,parser,url=inspect(f'http://{host}:2718/studio/lesson/')
    for frame in parser.frames:
        if frame.get('id')=='marimo-studio-editor':
            inspect(urljoin(url,frame['src']))
    inspect(f'http://{host}:2718/')
