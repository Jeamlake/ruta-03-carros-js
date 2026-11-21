"""Recursos originales de Ruta 03: sprites SVG y música/efectos WAV, sin archivos del profesor."""
from pathlib import Path
import math, random, struct, wave
ROOT=Path(__file__).resolve().parents[1]/'public/assets'

def svg(name, content, width=80, height=140):
    """Guarda un sprite vectorial con tamaño explícito para el cargador Phaser."""
    (ROOT/'img'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{content}</svg>',encoding='utf-8')

svg('jugador.svg','''<defs><linearGradient id="p" x2="1" y2="1"><stop stop-color="#ffb06c"/><stop offset="1" stop-color="#f45837"/></linearGradient></defs><ellipse cx="40" cy="75" rx="32" ry="61" fill="#000" opacity=".23"/><g fill="#102522"><rect x="7" y="27" width="14" height="29" rx="5"/><rect x="59" y="27" width="14" height="29" rx="5"/><rect x="7" y="91" width="14" height="29" rx="5"/><rect x="59" y="91" width="14" height="29" rx="5"/></g><path d="M24 7Q40 0 56 7L65 30 65 118Q63 133 52 134H28Q17 133 15 118V30Z" fill="url(#p)" stroke="#ffbc82" stroke-width="2"/><path d="M27 13H33V127H27ZM46 13H52V127H46Z" fill="#ffe3b5"/><path d="M23 53L29 36H51L57 53 54 72H26Z" fill="#183c40" stroke="#ffb985" stroke-width="2"/><path d="M27 57L31 41H49L53 57" fill="#5c9391"/><path d="M26 95H54L57 115H23Z" fill="#143938" stroke="#ffb985" stroke-width="2"/><path d="M30 99H50L52 108H28Z" fill="#598d87"/><path d="M19 15L28 12V24H18ZM52 12L61 15 62 24H52Z" fill="#fff8cc"/><path d="M20 125H28V130H20ZM52 125H60V130H52Z" fill="#a02524"/><path d="M30 78H50" stroke="#b54330" stroke-width="2"/>''')
svg('rival.svg','''<ellipse cx="40" cy="74" rx="33" ry="60" fill="#000" opacity=".2"/><g fill="#152426"><rect x="8" y="26" width="12" height="26" rx="4"/><rect x="60" y="26" width="12" height="26" rx="4"/><rect x="8" y="94" width="12" height="25" rx="4"/><rect x="60" y="94" width="12" height="25" rx="4"/></g><path d="M25 8Q40 2 55 8L64 26 63 122Q40 140 17 122L16 26Z" fill="#70b5bd" stroke="#b0e4dc" stroke-width="2"/><path d="M25 34H55L60 54 53 68H27L20 54Z" fill="#153842"/><path d="M28 39H52L56 51H24Z" fill="#5b8f9a"/><path d="M26 96H54L59 115H21Z" fill="#1b3847"/><path d="M25 18H55" stroke="#aedfd8" stroke-width="3"/><path d="M19 119H29V126H19ZM51 119H61V126H51Z" fill="#ed694a"/><path d="M20 13H28V24H20ZM52 13H60V24H52Z" fill="#fff3b4"/>''')
svg('camion.svg','''<ellipse cx="45" cy="87" rx="40" ry="79" fill="#000" opacity=".3"/><g fill="#081a23"><rect x="2" y="23" width="14" height="33" rx="4"/><rect x="74" y="23" width="14" height="33" rx="4"/><rect x="2" y="112" width="14" height="35" rx="4"/><rect x="74" y="112" width="14" height="35" rx="4"/></g><rect x="10" y="53" width="70" height="109" rx="7" fill="#7673b7" stroke="#bab0e9" stroke-width="2"/><path d="M19 8Q45 0 71 8L79 49H11Z" fill="#aaa1ea" stroke="#c9c9ff" stroke-width="2"/><path d="M23 14H67L72 33H18Z" fill="#143346"/><path d="M25 17H64L67 24H22Z" fill="#66a0b3"/><path d="M20 67H70M20 83H70M20 99H70M20 115H70M20 131H70" stroke="#504f86" stroke-width="3"/><path d="M17 153H28M62 153H73" stroke="#ff696c" stroke-width="6"/><path d="M14 42H25M65 42H76" stroke="#fff4c8" stroke-width="5"/>''',90,170)
for name,color,dark in [('barril.svg','#f6aa4d','#9f5e31'),('barrilRojo.svg','#ed6a70','#8e364e')]:
 svg(name,f'''<ellipse cx="35" cy="44" rx="29" ry="27" fill="#000" opacity=".24"/><rect x="10" y="10" width="50" height="54" rx="17" fill="{dark}"/><rect x="11" y="6" width="48" height="52" rx="16" fill="{color}" stroke="#f8d6a9" stroke-width="2"/><path d="M12 21H58M12 45H58" stroke="#4d4d45" stroke-width="5"/><ellipse cx="35" cy="13" rx="22" ry="8" fill="{color}" stroke="#ffe3c0" stroke-width="2"/><circle cx="45" cy="12" r="3" fill="{dark}"/><path d="M27 29L35 25 43 29 40 39H30Z" fill="#fff0c0" opacity=".8"/>''',70,76)
for level in [1,2]:
 road='#53655b' if level==1 else '#233541'
 verge='#d6b485' if level==1 else '#142636'
 lines='#eae3bb' if level==1 else '#51c8c6'
 items=[]
 rng=random.Random(level)
 for y in range(-40,850,140):
  for x in [22,536]:
   if level==1:
    items.append(f'<ellipse cx="{x+20}" cy="{y+50}" rx="24" ry="12" fill="#ba976a"/><path d="M{x+20} {y+52}v-30" stroke="#8b7950" stroke-width="6"/><path d="M{x} {y+30}q20-38 42 0q-18-15-21 1q-9-17-21-1" fill="#536a47"/>')
   else:
    items.append(f'<rect x="{x-10}" y="{y}" width="60" height="90" rx="5" fill="#1d3c4d" stroke="#2d6776"/><path d="M{x} {y+15}h12m8 0h12m-32 20h12m8 0h12m-32 20h12m8 0h12" stroke="#efbf77" stroke-width="4"/>')
 marks=''.join(f'<path d="M233 {y}v54M367 {y}v54" stroke="{lines}" stroke-width="5"/>' for y in range(0,821,100))
 edges=''.join(f'<rect x="88" y="{y}" width="12" height="20" fill="{lines}"/><rect x="500" y="{y}" width="12" height="20" fill="{lines}"/>' for y in range(0,821,40))
 svg(f'fondo{level}.svg',f'<rect width="600" height="820" fill="{verge}"/><rect x="100" width="400" height="820" fill="{road}"/><path d="M116 0v820M484 0v820" stroke="{lines}" stroke-width="3"/>{marks}{edges}'+''.join(items),600,820)

SR=22050
def wav(name, duration, callback):
    """Escribe PCM original con limitación de amplitud para evitar saturación."""
    samples=[max(-.95,min(.95,callback(i/SR))) for i in range(round(SR*duration))]
    with wave.open(str(ROOT/'audio'/name),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h',round(s*32767)) for s in samples))

for level,notes in [(1,[64,67,69,67,62,64,67,62]),(2,[57,60,64,67,64,60,62,59])]:
 def melody(t,notes=notes,level=level):
    step=.22 if level==2 else .29
    index=int(t/step);phase=t%step;freq=440*2**((notes[index%8]-69)/12)
    envelope=min(1,phase/.008)*math.exp(-phase*7)
    lead=(math.sin(2*math.pi*freq*t)+.22*math.sin(4*math.pi*freq*t))*.12*envelope
    bass=math.sin(2*math.pi*(freq/4)*t)*.08*math.exp(-(t%(step*2))*7)
    kick=math.sin(2*math.pi*(58*t+2*(1-math.exp(-60*(t%(step*2))))))*.08*math.exp(-(t%(step*2))*35)
    return (lead+bass+kick)*min(1,t/.05)
 wav(f'musica{level}.wav',8*(.22 if level==2 else .29)*4,melody)
for name,freq in [('choque-carro.wav',130),('choque-barril.wav',230)]:
 rng=random.Random(freq);noise=[rng.uniform(-1,1) for _ in range(int(SR*.32)+1)]
 wav(name,.32,lambda t,f=freq:(noise[min(len(noise)-1,int(t*SR))]*.25+math.sin(2*math.pi*f*t)*.18)*math.exp(-t*12))
wav('punto.wav',.16,lambda t:math.sin(2*math.pi*950*t)*.1*math.exp(-t*20))
wav('nivel.wav',.8,lambda t:math.sin(2*math.pi*[523,659,784,1047][min(3,int(t/.2))]*t)*.16*math.exp(-(t%.2)*9))
print('Recursos originales generados en',ROOT)
