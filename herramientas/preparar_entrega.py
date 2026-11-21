"""Prepara el PDF de enlaces y las evidencias reales disponibles de Ruta 03.
No transforma capturas en estados no observados ni incluye documentos privados del curso.
"""
from pathlib import Path
import shutil, zipfile, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ACA=Path(r'C:\Ayudix\Estudios\Videojuegos-I\Juego-Carros-20261120')
ENT=ROOT/'public/entrega'; CAPS=ENT/'capturas'
CAPS.mkdir(parents=True,exist_ok=True)
BASE='https://jeamlake.github.io/ruta-03-carros-js/'
REPO='https://github.com/Jeamlake/ruta-03-carros-js'
AUTOR='José Eduardo Alvarado Mejía'
for name in ['portada-celular.jpg','nivel-1-completo.jpg','transicion-inicial.jpg','derrota-completo.jpg']:
    shutil.copy2(ACA/'qa'/name,CAPS/name)
video=Path(r'C:\Users\USER\Downloads\Ruta03-Partida-Jose-Eduardo.webm')
if video.exists():shutil.copy2(video,ENT/'Ruta03_Demostracion.webm')

(ENT/'demostracion.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Demostración de Ruta 03</title><style>body{margin:0;background:#101e19;color:#f5f0e8;font:16px/1.6 "Segoe UI",Arial,sans-serif}main{max-width:850px;margin:40px auto;padding:0 24px}h1{font-size:38px;line-height:1.1}a{color:#ffb282}video{display:block;max-width:100%;max-height:75vh;margin:25px auto;background:#071a14;border-radius:12px}p{color:#bacabb}.nota{border-left:3px solid #ff9167;padding-left:15px;font-size:14px}</style><main><a href="../">← Volver al juego</a><h1>Ruta 03 en movimiento</h1><p>José Eduardo Alvarado Mejía · Juego de carros con JavaScript y Phaser CE.</p><video controls playsinline preload="metadata"><source src="Ruta03_Demostracion.webm" type="video/webm">Tu navegador no reproduce este formato. Usa el enlace de descarga.</video><p><a href="Ruta03_Demostracion.webm" download>Descargar video grabado</a> · <a href="galeria.html">Ver capturas</a></p><p class="nota">Grabación real de una prueba del primer nivel y del estado de derrota. Para registrar otro recorrido, el juego incluye Grabar partida y Guardar captura; no utiliza cámara ni micrófono.</p></main></html>''',encoding='utf-8')
cards=[('Portada en celular','portada-celular.jpg'),('Primer nivel en ejecución','nivel-1-completo.jpg'),('Transición al segundo nivel con tres puntos','transicion-inicial.jpg'),('Derrota y opción de reintento','derrota-completo.jpg')]
gallery=''.join(f'<section><h2>{title}</h2><a href="capturas/{name}"><img src="capturas/{name}" alt="{title}"></a></section>' for title,name in cards)
(ENT/'galeria.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Capturas de Ruta 03</title><style>body{background:#101e19;color:#f5f0e8;font:16px/1.6 "Segoe UI",Arial,sans-serif;margin:25px}main{max-width:1100px;margin:auto}a{color:#ffb282}img{width:100%;height:auto;border-radius:12px}section{margin:32px 0}h1{font-size:38px}h2{font-size:20px}</style><main><a href="../">← Volver al juego</a><h1>Evidencias de Ruta 03</h1><p>Capturas reales del prototipo. Pulsa una imagen para verla en su tamaño original.</p>'''+gallery+'</main></html>',encoding='utf-8')

pdfmetrics.registerFont(TTFont('ArialRuta',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialRutaBold',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet()
for name in ['Normal','BodyText','Heading1','Heading2','Title']:
    styles[name].fontName='ArialRuta';styles[name].textColor=colors.HexColor('#17392f')
styles['Normal'].fontSize=10;styles['Normal'].leading=15;styles['Normal'].spaceAfter=8
styles['Title'].fontName='ArialRutaBold';styles['Title'].fontSize=34;styles['Title'].leading=39;styles['Title'].spaceAfter=14
styles['Heading1'].fontName='ArialRutaBold';styles['Heading1'].fontSize=18;styles['Heading1'].leading=23;styles['Heading1'].spaceBefore=10;styles['Heading1'].spaceAfter=10
styles['Heading2'].fontName='ArialRutaBold';styles['Heading2'].fontSize=12;styles['Heading2'].leading=17;styles['Heading2'].spaceBefore=7;styles['Heading2'].spaceAfter=5
styles.add(ParagraphStyle('PequenoRuta',parent=styles['Normal'],fontSize=8.5,leading=12))
styles.add(ParagraphStyle('CentroRuta',parent=styles['Normal'],alignment=TA_CENTER,fontSize=9,leading=13))

def P(text,style='Normal'):return Paragraph(text,styles[style])
def link(label,url):return P(f'<b>{label}</b><br/><link href="{url}" color="#a5482e">{url}</link>','PequenoRuta')

class Captura(Flowable):
    """Recorte de maquetación en PDF; conserva intacto el archivo original enlazado."""
    def __init__(self,path,rect,width=200):
        super().__init__();self.path=str(path);self.rect=rect;self.width=width;self.height=width*rect[3]/rect[2]
    def draw(self):
        x,y,w,h=self.rect; iw,ih=Image.open(self.path).size;s=self.width/w;c=self.canv
        c.saveState();clip=c.beginPath();clip.rect(0,0,self.width,self.height);c.clipPath(clip,stroke=0,fill=0)
        c.drawImage(ImageReader(self.path),-x*s,self.height-(ih-y)*s,width=iw*s,height=ih*s)
        c.restoreState()

def pagina(c,doc):
    c.setStrokeColor(colors.HexColor('#d7e0d7'));c.line(44,42,568,42)
    c.setFont('ArialRuta',8);c.setFillColor(colors.HexColor('#56685c'))
    c.drawString(44,27,'Ruta 03 | José Eduardo Alvarado Mejía');c.drawRightString(568,27,f'{doc.page}')

story=[P('UNIVERSIDAD TECNOLÓGICA DEL PERÚ','Heading2'),P('Diseño y Desarrollo de Juegos Interactivos I<br/>Sección 45350 - Periodo 2026-II','Normal'),Spacer(1,25),P('RUTA 03','Title'),P('Juego de carros en JavaScript con dos niveles','Heading1'),P('<b>Estudiante</b><br/>'+AUTOR),P('<b>Fecha</b><br/>20 de noviembre de 2026'),Spacer(1,14),P('Enlaces del proyecto','Heading1')]
for label,url in [('Juego publicado en GitHub Pages',BASE),('Repositorio y archivos editables',REPO),('Descarga del código del repositorio',REPO+'/archive/refs/heads/main.zip'),('Video grabado durante las pruebas',BASE+'entrega/demostracion.html'),('Galería de capturas',BASE+'entrega/galeria.html')]:story.append(link(label,url))
story+=[Spacer(1,12),P('La versión publicada funciona desde un navegador de PC o celular y no requiere mantener encendida la computadora del autor. El proyecto incluye una copia HTML autónoma para jugar sin servidor.','PequenoRuta'),PageBreak(),P('Diseño y funcionamiento','Heading1'),P('Objetivo: conducir por dos escenarios evitando vehículos y barriles. Cada obstáculo esquivado suma un punto. Un impacto resta una vida y no concede puntos. La posición del jugador se mantiene dentro de la carretera.'),P('Progresión de los niveles','Heading2')]
rows=[['Elemento','Nivel 1','Nivel 2'],['Escenario','Costa al amanecer','Ciudad de neón'],['Obstáculos','Autos y barriles naranjas','Camiones y barriles rojos'],['Velocidad base','230 píxeles por segundo','355 píxeles por segundo'],['Intervalo de aparición','2,15 segundos','1,55 segundos'],['Objetivo','Llegar a 3 puntos','Llegar a 6 puntos acumulados']]
table=Table([[P(x,'PequenoRuta') for x in row] for row in rows],colWidths=[130,197,197],hAlign='LEFT')
table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5ede3')),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#cbd7cb')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story +=[table,Spacer(1,12),P('Controles y condiciones de cierre','Heading2'),P('Flechas o W, A, S y D para mover el carro. En celular se puede arrastrar el jugador o usar los botones de cambio de carril. P o Escape pausa. La partida también se pausa al ocultar la pestaña. Con cero vidas se muestra VUELVE A INTENTARLO; con seis puntos, GANASTE. Reintentar reinicia puntos, vidas y nivel.'),P('Elementos solicitados implementados','Heading2'),P('Portada con nombre y apellido; tres vidas; contador de puntos; música de fondo; efectos diferenciados al chocar con vehículos o barriles; detección de colisiones; dos niveles con obstáculos y velocidad distintos; transición a tres puntos; victoria y derrota.'),P('Mejoras de presentación y uso','Heading2'),P('Sprites y música originales, diseño adaptable, protección de 1,25 segundos después de un impacto, efecto visual de choque, pausa, captura PNG y grabación de Canvas con audio. La grabación no requiere acceso al micrófono, la cámara o la pantalla del usuario.'),P('Relación con los contenidos de clase','Heading2'),P('Semana 2: gameplay, controles y presentación. Semana 9: GUI, entidades y HUD. Semana 12: Phaser, sprites y ciclo preload/create/update. Semana 13: colisiones 2D. El enunciado solicita JavaScript; por ello se usa Phaser CE, aunque las primeras sesiones del curso también trabajaron con Unity.','PequenoRuta'),PageBreak(),P('Evidencias del prototipo','Heading1'),P('Capturas reales de la portada, la jugabilidad inicial, el cambio de etapa y la derrota. Los archivos completos se pueden abrir desde la galería enlazada.','PequenoRuta')]
rects=[(15,188,331,453),(703,126,449,615),(703,126,449,615),(703,126,449,615)]
cells=[]
for (title,name),rect in zip(cards,rects):
    cells.append([Captura(CAPS/name,rect,188),Spacer(1,5),P(title,'CentroRuta')])
gallerytable=Table([[cells[0],cells[1]],[cells[2],cells[3]]],colWidths=[262,262])
gallerytable.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(0,0),(-1,-1),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),25),('RIGHTPADDING',(0,0),(-1,-1),25),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
story.append(gallerytable)
pdf=ENT/'Entrega_Jose_Eduardo_Alvarado_Mejia.pdf'
SimpleDocTemplate(str(pdf),pagesize=(612,792),leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=54,title='Ruta 03 - Juego de carros',author=AUTOR).build(story,onFirstPage=pagina,onLaterPages=pagina)
shutil.copy2(pdf,ACA/pdf.name)
(ROOT/'ABRIR-JUEGO.cmd').write_text('@echo off\nstart "" "%~dp0public\\JUGAR-SIN-INSTALAR.html"\n',encoding='ascii')
(ACA/'ESTADO-ENTREGA.txt').write_text('''RUTA 03 - ESTADO DE LA ENTREGA\nEstudiante: José Eduardo Alvarado Mejía\n\nEl juego implementa la consigna de carros de la imagen (10 puntos). El usuario confirmó que hay otra pregunta: su contenido no se ha recibido.\n\nVerificado: 14 pruebas de reglas, portada y adaptación móvil, ejecución de primer nivel, choques, derrota, transición a tres puntos y entrada al nivel dos con pausa y velocidad 355.\n\nPendiente de ampliar antes de considerar toda la evidencia final: captura del segundo nivel en ejecución, recorrido grabado completo hasta GANASTE y comprobación final de los botones táctiles tras su ajuste a eventos click. El video incluido registra una prueba real del primer nivel y derrota.\n\nLa herramienta de control del navegador se detuvo por su verificación de seguridad al no poder determinar con confianza la URL. No se eludió ese bloqueo. Se continuó con archivos, pruebas y GitHub por herramientas de desarrollo.\n\nPublicación: https://jeamlake.github.io/ruta-03-carros-js/\nRepositorio: https://github.com/Jeamlake/ruta-03-carros-js\n''',encoding='utf-8-sig')
(ACA/'EXPLICACION-PARA-EXPONER.txt').write_text('''GUÍA PARA EXPLICAR RUTA 03\nJosé Eduardo Alvarado Mejía\n\nMi juego está desarrollado en JavaScript con Phaser CE, siguiendo el patrón que trabajamos en la guía de la semana 12. La portada tiene mi nombre y muestra el objetivo. El personaje es un carro y los obstáculos son vehículos y barriles.\n\nEn preload cargo los sprites locales. En create construyo el fondo, los grupos de obstáculos, el jugador con su cuerpo físico, el HUD y los controles. En update proceso la entrada, desplazo los obstáculos y el escenario, compruebo colisiones y actualizo la interfaz.\n\nHUD significa interfaz de información durante la partida: en este caso muestra vidas, puntos y nivel. Los sprites son las imágenes de los objetos del juego. Arcade Physics detecta cuándo el cuerpo físico del jugador se superpone con un obstáculo. El cuerpo físico es un poco menor que la imagen para que las colisiones sean justas visualmente.\n\nEl módulo reglas.js separa las reglas del dibujo. Contiene las funciones para empezar, sumar puntos, recibir impactos, pausar, continuar y pasar al segundo nivel. Con esta separación puedo probar las reglas sin necesitar un navegador. Incluí 14 pruebas automáticas.\n\nComienzo con tres vidas. Cuando un obstáculo sale por la parte inferior sin ser golpeado, suma un punto. Si se produce una colisión, se elimina el obstáculo, se resta una vida y se reproduce un sonido. Durante 1,25 segundos se protege al jugador para que un mismo choque no consuma varias vidas.\n\nAl conseguir tres puntos, el juego entra al estado de transición. Después de continuar comienza el nivel dos con los mismos puntos y vidas. El escenario cambia a una ciudad nocturna, aparecen camiones y barriles rojos y la velocidad base aumenta de 230 a 355 píxeles por segundo. Al llegar a seis puntos acumulados aparece GANASTE. Si las vidas llegan a cero aparece VUELVE A INTENTARLO.\n\nEl juego admite teclado y controles táctiles. La pausa conserva la partida. El sonido se inicia después de una acción del usuario porque los navegadores restringen el audio automático. Los archivos de música y los sprites se incluyen en el proyecto para no depender de recursos remotos.\n\nLa publicación usa GitHub Pages. La carpeta public contiene el sitio. Un flujo de GitHub Actions ejecuta las pruebas y publica esa carpeta cuando actualizo la rama main. Por eso el enlace funciona aunque mi computadora esté apagada. También incluyo un HTML autónomo para jugar sin servidor.\n\nPara mostrar el código al profesor, abriría primero principal.js para explicar preload, create y update; luego reglas.js para mostrar el cambio exacto de nivel y las vidas; y finalmente sonido.js para explicar música y efectos. Las funciones nuevas llevan comentarios sobre su responsabilidad y relación con los otros archivos.\n''',encoding='utf-8-sig')
print(json.dumps({'pdf':str(pdf),'video_bytes':(ENT/'Ruta03_Demostracion.webm').stat().st_size},ensure_ascii=False))
