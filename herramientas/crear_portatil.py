"""Genera una copia HTML autónoma del mismo juego, conservando aparte los fuentes editables."""
from pathlib import Path
import base64,json
ROOT=Path(__file__).resolve().parents[1]/'public'
recursos={}
for folder,ext,mime in [('img','.svg','image/svg+xml'),('audio','.wav','audio/wav')]:
 for p in (ROOT/'assets'/folder).glob('*'+ext):
  recursos[p.stem]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
html=(ROOT/'index.html').read_text(encoding='utf-8')
html=html.replace('<link rel="stylesheet" href="estilos.css">','<style>'+(ROOT/'estilos.css').read_text(encoding='utf-8')+'</style>')
html=html.replace('<link rel="icon" href="assets/img/jugador.svg" type="image/svg+xml">','')
html=html.replace('<script defer src="vendor/phaser.min.js"></script>','<script>'+ (ROOT/'vendor/phaser.min.js').read_text(encoding='utf-8').replace('</script','<\\/script')+'</script>')
for name in ['reglas.js','sonido.js','principal.js']:
 html=html.replace(f'<script defer src="{name}"></script>','')
scripts='<script>window.RUTA_RECURSOS='+json.dumps(recursos)+';</script>'
for name in ['reglas.js','sonido.js','principal.js']:
 scripts+='<script>'+ (ROOT/name).read_text(encoding='utf-8').replace('</script','<\\/script')+'</script>'
html=html.replace('</body>',scripts+'</body>')
(ROOT/'JUGAR-SIN-INSTALAR.html').write_text(html,encoding='utf-8')
print('HTML portátil creado:',len(html),'caracteres')
