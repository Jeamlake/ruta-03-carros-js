"""Servidor local de Ruta 03. Publica solo public/, sin listado de carpetas ni archivos ocultos."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, urlsplit
import argparse, functools
ROOT=Path(__file__).resolve().parent/'public'
class Handler(SimpleHTTPRequestHandler):
    """Restringe la navegación al sitio entregable y evita publicar los archivos de trabajo."""
    def send_head(self):
        path=unquote(urlsplit(self.path).path)
        if any(p.startswith('.') or p=='..' for p in path.split('/') if p):
            self.send_error(404);return None
        return super().send_head()
    def list_directory(self,path):
        self.send_error(404);return None
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('X-Robots-Tag','noindex, nofollow, noarchive')
        self.send_header('Cache-Control','no-cache')
        super().end_headers()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--puerto',type=int,default=8795);a=p.parse_args()
    print(f'Ruta 03: http://127.0.0.1:{a.puerto}/',flush=True)
    ThreadingHTTPServer(('127.0.0.1',a.puerto),functools.partial(Handler,directory=str(ROOT))).serve_forever()
