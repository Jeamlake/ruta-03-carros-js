/** Ruta 03: juego de carros de José Eduardo Alvarado Mejía.
 * Sigue preload/create/update de Phaser CE, como la guía de semana 12 del curso.
 * Regla y progresión: reglas.js. Música y grabación: sonido.js y MediaRecorder.
 * Los choques se detectan con Arcade Physics; ningún botón concede puntos ni vidas. */
(function(){
 'use strict';
 const R=window.ReglasRuta,W=600,H=820;
 const autor='José Eduardo Alvarado Mejía';
 const dom={juego:document.querySelector('#juego'),accion:document.querySelector('#accion'),pausa:document.querySelector('#pausa'),estado:document.querySelector('#estado'),sonido:document.querySelector('#sonido'),grabar:document.querySelector('#grabar')};
 const audio=new SonidoRuta();
 let partida=R.nuevaPartida(),game,fondo,jugador,obstaculos,hud,capa,polvo,teclas;
 let siguiente=1.1,secuencia=0,desplazamiento=0,arrastrando=false,offset={x:0,y:0},ultimoEstado='',grabador=null,trozos=[],urlVideo=null;
 const patron={1:[1,0,1,2,1,0,2,1],2:[1,2,1,0,1,2,0,1]};
 const posiciones=[170,300,430];
 /** Texto de Canvas para que el HUD, nombre y estados también aparezcan en el video. */
 function texto(grupo,x,y,contenido,tamano=20,color='#f7efda',centrado=false){
   const t=game.add.text(x,y,contenido,{font:`${tamano}px Arial`,fill:color,align:centrado?'center':'left'},grupo);
   if(centrado)t.anchor.set(.5,0);return t;
 }
 /** Precarga todos los gráficos desde el proyecto, nunca desde una URL externa. */
 function preload(){
   game.stage.backgroundColor='#17291f';
   ['jugador','rival','camion','barril','barrilRojo','fondo1','fondo2'].forEach(k=>game.load.image(k,window.RUTA_RECURSOS?.[k]||'assets/img/'+k+'.svg'));
   game.load.onFileError.add(k=>{console.error('Recurso no cargado: '+k);document.querySelector('#fallo').hidden=false;});
 }
 /** Construye las capas en orden: fondo, obstáculos, jugador, HUD, mensajes. */
 function create(){
   game.stage.disableVisibilityChange=true;
   game.physics.startSystem(Phaser.Physics.ARCADE);
   fondo=game.add.tileSprite(0,0,W,H,'fondo1');
   obstaculos=game.add.group();obstaculos.enableBody=true;obstaculos.physicsBodyType=Phaser.Physics.ARCADE;
   jugador=game.add.sprite(300,678,'jugador');jugador.anchor.set(.5);jugador.scale.set(.8);
   game.physics.arcade.enable(jugador);jugador.body.setSize(48,112,16,12);
   polvo=game.add.group();
   hud=game.add.group();const banda=game.add.graphics(0,0,hud);
   banda.beginFill(0x10231f,.97);banda.drawRect(0,0,600,95);banda.drawRect(0,781,600,39);banda.endFill();
   texto(hud,27,15,'VIDAS',12,'#abc3ad');hud.vidas=texto(hud,24,36,'♥ ♥ ♥',29,'#ff966d');
   texto(hud,238,15,'PUNTOS',12,'#abc3ad');hud.puntos=texto(hud,233,35,'00 / 03',29);
   texto(hud,445,15,'NIVEL',12,'#abc3ad');hud.nivel=texto(hud,445,35,'01 / 02',27);
   texto(hud,300,791,autor,15,'#d7e2cb',true);
   capa=game.add.group();
   teclas=game.input.keyboard.addKeys({izq:Phaser.Keyboard.LEFT,der:Phaser.Keyboard.RIGHT,arriba:Phaser.Keyboard.UP,abajo:Phaser.Keyboard.DOWN,a:Phaser.Keyboard.A,d:Phaser.Keyboard.D,w:Phaser.Keyboard.W,s:Phaser.Keyboard.S});
   game.input.keyboard.addKeyCapture([37,38,39,40,32]);
   game.input.keyboard.addKey(Phaser.Keyboard.P).onDown.add(pausar);
   game.input.keyboard.addKey(Phaser.Keyboard.ESC).onDown.add(pausar);
   game.input.onDown.add(p=>{if(partida.estado==='jugando'&&p.y>95&&p.y<780){arrastrando=true;offset={x:jugador.x-p.x,y:jugador.y-p.y};}});
   game.input.onUp.add(()=>{arrastrando=false;});
   dom.accion.disabled=false;dom.grabar.disabled=!window.MediaRecorder;sincronizar(true);
 }
 /** Un obstáculo por oleada: siempre quedan carriles transitables. Nivel 2 cambia tipos y velocidad. */
 function generar(){
   const cfg=R.NIVELES[partida.nivel],lane=patron[partida.nivel][secuencia%8];
   const tipo=cfg.tipos[secuencia%2];
   let o=obstaculos.children.find(s=>!s.alive&&s.key===tipo);
   if(o)o.reset(posiciones[lane],-100);else{o=obstaculos.create(posiciones[lane],-100,tipo);o.anchor.set(.5);}
   o.scale.set(tipo==='camion'?.78:tipo.startsWith('barril')?.85:.8);
   o.body.enable=true;o.body.allowGravity=false;
   if(tipo==='camion')o.body.setSize(66,145,12,10);
   else if(tipo.startsWith('barril'))o.body.setSize(46,48,12,9);
   else o.body.setSize(49,112,16,12);
   o.velocidad=cfg.velocidad+(secuencia%3)*12;o.body.velocity.y=o.velocidad;o.tipo=tipo;
   secuencia++;
 }
 /** Recorta el movimiento a la carretera; el jugador nunca puede salirse por los bordes. */
 function limitar(){jugador.x=Phaser.Math.clamp(jugador.x,136,464);jugador.y=Phaser.Math.clamp(jugador.y,185,710);}
 /** Actualización basada en segundos, con pausa y límite de delta para evitar saltos tras un bloqueo. */
 function update(){
   if(!jugador)return;
   const dt=Math.min(.05,game.time.elapsedMS/1000||0);
   jugador.body.velocity.set(0);
   if(partida.estado==='jugando'){
     partida=R.avanzar(partida,dt);desplazamiento+=R.NIVELES[partida.nivel].velocidad*dt*.65;
     fondo.tilePosition.y=desplazamiento;
     obstaculos.forEachAlive(o=>{o.body.velocity.y=o.velocidad;});
     if(arrastrando){const p=game.input.activePointer;jugador.body.reset(Phaser.Math.clamp(p.x+offset.x,136,464),Phaser.Math.clamp(p.y+offset.y,185,710));}
     else{
       const dx=Number(teclas.der.isDown||teclas.d.isDown)-Number(teclas.izq.isDown||teclas.a.isDown);
       const dy=Number(teclas.abajo.isDown||teclas.s.isDown)-Number(teclas.arriba.isDown||teclas.w.isDown);
       const normal=dx&&dy?Math.SQRT1_2:1;jugador.body.velocity.set(dx*340*normal,dy*340*normal);
     }
     limitar();jugador.alpha=partida.invulnerable>0?(Math.floor(partida.tiempo*13)%2?.45:1):1;
     siguiente-=dt;if(siguiente<=0){generar();siguiente=R.NIVELES[partida.nivel].intervalo;}
     // El callback elimina el objeto impactado antes de que pueda otorgar puntos.
     game.physics.arcade.overlap(jugador,obstaculos,colision,null,this);
     obstaculos.forEachAlive(o=>{if(o.y>H+100&&partida.estado==='jugando'){
       o.kill();partida=R.puntuar(partida);audio.efecto('punto');sincronizar();
       if(partida.estado!=='jugando')obstaculos.callAll('kill');
     }});
   }else{
     obstaculos.forEachAlive(o=>o.body.velocity.set(0));jugador.alpha=1;
   }
   limitar();sincronizar();
 }
 /** Un choque válido resta una vida y reproduce un efecto diferente para vehículos y barriles. */
 function colision(p,o){
   if(partida.estado!=='jugando'||partida.invulnerable>0)return;
   const anterior=partida.vidas;partida=R.chocar(partida);o.kill();
   if(partida.vidas===anterior)return;
   audio.efecto(o.tipo.startsWith('barril')?'choque-barril':'choque-carro');
   game.camera.shake(.004,150);game.camera.flash(0xffa15b,120);
   for(let i=0;i<10;i++){
     const chispa=game.add.graphics(p.x,p.y,polvo);chispa.beginFill(i%2?0xffce70:0xff7853);chispa.drawRect(-3,-3,6,6);chispa.endFill();
     game.add.tween(chispa).to({x:p.x+game.rnd.between(-85,85),y:p.y+game.rnd.between(-75,55),alpha:0},450,Phaser.Easing.Quadratic.Out,true).onComplete.add(()=>chispa.destroy());
   }
   dom.estado.textContent=`Choque. ${partida.vidas} ${partida.vidas===1?'vida restante':'vidas restantes'}.`;
   sincronizar(true);
 }
 /** Mensajes de portada, transición, pausa, victoria y derrota dibujados en Canvas para el video. */
 function mensaje(){
   capa.removeAll(true);const s=partida.estado;if(s==='jugando')return;
   const sombra=game.add.graphics(0,0,capa);sombra.beginFill(0x0c211d,.94);sombra.drawRect(0,95,W,686);sombra.endFill();
   const datos={
     portada:['ELIGE TU RUTA','RUTA 03','Tres vidas. Dos niveles. Una meta.','Cada obstáculo superado suma un punto.\n3 para el nivel 2. 6 para ganar.'],
     transicion:['PRIMER TRAMO COMPLETADO','NIVEL 2','Ciudad de neón','3 puntos conseguidos.\nNuevos obstáculos. Más velocidad.'],
     pausa:['UN MOMENTO EN BOXES','PAUSA','Tu partida te está esperando.','Los puntos y las vidas se conservan.\nContinúa cuando estés listo.'],
     ganaste:['META ALCANZADA','GANASTE','¡Completaste las dos rutas!','6 puntos y '+partida.vidas+' '+(partida.vidas===1?'vida restante.':'vidas restantes.')],
     perdiste:['VUELVE A LA PISTA','VUELVE A\nINTENTARLO','Te quedaste sin vidas.','Puntos conseguidos: '+partida.puntos+' / 6\nCada intento es una nueva carrera.']
   }[s];
   texto(capa,300,179,datos[0],14,'#c8c99e',true);
   const titulo=texto(capa,300,s==='perdiste'?240:244,datos[1],s==='perdiste'?48:67,s==='ganaste'?'#b8ec9b':'#ff9b65',true);titulo.fontWeight='bold';
   texto(capa,300,s==='perdiste'?363:338,datos[2],22,'#f7efda',true);
   texto(capa,300,s==='perdiste'?411:386,datos[3],18,'#c0d0ba',true);
   const coche=game.add.sprite(300,532,s==='transicion'?'camion':'jugador',null,capa);coche.anchor.set(.5);coche.scale.set(s==='transicion'?.58:.75);coche.angle=-9;
   texto(capa,300,724,'UN JUEGO DE JOSÉ EDUARDO ALVARADO MEJÍA',12,'#dce5cb',true);
   texto(capa,300,752,'FLECHAS · W A S D · CONTROLES TÁCTILES',11,'#879f8f',true);
 }
 /** Refleja el modelo en el HUD, controles semánticos y atributos de inspección solo de lectura. */
 function sincronizar(forzar=false){
   hud.vidas.text='♥ '.repeat(partida.vidas)+'♡ '.repeat(3-partida.vidas);
   hud.puntos.text=String(partida.puntos).padStart(2,'0')+' / '+String(R.NIVELES[partida.nivel].meta).padStart(2,'0');
   hud.nivel.text='0'+partida.nivel+' / 02';
   dom.juego.dataset.estado=partida.estado;dom.juego.dataset.puntos=partida.puntos;dom.juego.dataset.vidas=partida.vidas;dom.juego.dataset.nivel=partida.nivel;
   dom.juego.dataset.velocidad=R.NIVELES[partida.nivel].velocidad;
   dom.juego.dataset.jugador=JSON.stringify({x:Math.round(jugador.x),y:Math.round(jugador.y)});
   dom.juego.dataset.obstaculos=JSON.stringify(obstaculos.children.filter(o=>o.alive).map(o=>({tipo:o.tipo,x:Math.round(o.x),y:Math.round(o.y)})));
   if(!forzar&&ultimoEstado===partida.estado)return;
   ultimoEstado=partida.estado;mensaje();
   const labels={portada:'Comenzar la carrera →',transicion:'Entrar al nivel 2 →',pausa:'Continuar la carrera →',ganaste:'Volver a jugar →',perdiste:'Reintentar la carrera →'};
   dom.accion.hidden=partida.estado==='jugando';dom.accion.textContent=labels[partida.estado]||'';
   dom.pausa.disabled=!['jugando','pausa'].includes(partida.estado);dom.pausa.textContent=partida.estado==='pausa'?'▶':'Ⅱ';
   dom.pausa.setAttribute('aria-label',partida.estado==='pausa'?'Reanudar partida':'Pausar partida');
   document.querySelector('#etapa1').classList.toggle('actual',partida.nivel===1);
   document.querySelector('#etapa2').classList.toggle('actual',partida.nivel===2);
   const mensajes={portada:'Tres vidas. Dos niveles. Una meta.',jugando:`Nivel ${partida.nivel} · Esquiva para sumar puntos.`,transicion:'3 puntos. Nivel 1 completado.',pausa:'Partida pausada.',ganaste:'GANASTE. Completaste los dos niveles.',perdiste:'VUELVE A INTENTARLO. Sin vidas.'};
   dom.estado.textContent=mensajes[partida.estado];
   if(partida.estado==='transicion'||partida.estado==='ganaste'){audio.parar();audio.efecto('nivel');}
   else if(['pausa','perdiste'].includes(partida.estado))audio.parar();
 }
 /** Comienza/reintenta desde cero, o continúa exactamente el estado que muestra el botón. */
 async function accion(){
   dom.accion.disabled=true;
   try{await audio.iniciar();}catch(e){console.warn('Audio no disponible',e);dom.sonido.textContent='Sonido no disponible';}
   if(['portada','perdiste','ganaste'].includes(partida.estado)){
     partida=R.empezar();obstaculos.callAll('kill');siguiente=1.2;secuencia=0;desplazamiento=0;fondo.loadTexture('fondo1');jugador.body.reset(300,678);
   }else if(partida.estado==='transicion'){
     partida=R.segundoNivel(partida);siguiente=1;secuencia=0;fondo.loadTexture('fondo2');jugador.body.reset(300,678);
   }else if(partida.estado==='pausa')partida=R.reanudar(partida);
   arrastrando=false;audio.musica(partida.nivel);sincronizar(true);dom.accion.disabled=false;
 }
 /** Pausa explícita o automática al ocultar la pestaña; no pierde progreso ni vidas. */
 function pausar(){
   arrastrando=false;
   if(partida.estado==='jugando')partida=R.pausar(partida);
   else if(partida.estado==='pausa'){partida=R.reanudar(partida);audio.musica(partida.nivel);}
   sincronizar(true);
 }
 /** Los botones táctiles cambian de carril sin requerir mantener el dedo ni precisión al tocar. */
 function moverCarril(direccion){
   if(partida.estado!=='jugando')return;
   const actual=posiciones.reduce((a,b)=>Math.abs(a-jugador.x)<Math.abs(b-jugador.x)?a:b);
   const i=posiciones.indexOf(actual),destino=posiciones[Math.max(0,Math.min(2,i+direccion))];
   jugador.body.reset(destino,jugador.y);arrastrando=false;
 }
 /** Graba Canvas y audio del propio juego; no solicita cámara, micrófono ni captura de pantalla. */
 async function grabar(){
   const aviso=document.querySelector('#grabacion-estado');
   if(grabador&&grabador.state==='recording'){grabador.stop();return;}
   if(!game.canvas.captureStream||!window.MediaRecorder){aviso.textContent='Este navegador no permite grabar el juego. Puedes jugar normalmente.';return;}
   try{
     await audio.iniciar();const stream=game.canvas.captureStream(30);
     if(audio.salida)audio.salida.stream.getAudioTracks().forEach(t=>stream.addTrack(t.clone()));
     const tipo=['video/mp4;codecs=avc1.42001E,mp4a.40.2','video/mp4','video/webm;codecs=vp8,opus','video/webm'].find(t=>MediaRecorder.isTypeSupported(t));
     grabador=new MediaRecorder(stream,{...(tipo?{mimeType:tipo}:{}),videoBitsPerSecond:1800000});trozos=[];
     grabador.ondataavailable=e=>{if(e.data.size)trozos.push(e.data);};
     grabador.onstop=()=>{
       const blob=new Blob(trozos,{type:grabador.mimeType||'video/webm'});
       if(urlVideo)URL.revokeObjectURL(urlVideo);urlVideo=URL.createObjectURL(blob);
       const enlace=document.querySelector('#descarga-grabacion');enlace.href=urlVideo;enlace.download='Ruta03-Partida-Jose-Eduardo.'+(blob.type.includes('mp4')?'mp4':'webm');enlace.hidden=false;
       dom.grabar.textContent='● Grabar partida';dom.grabar.setAttribute('aria-pressed','false');aviso.textContent='Video listo. Guarda tu recorrido con el enlace de abajo.';
       stream.getTracks().forEach(t=>t.stop());
     };
     grabador.start(1000);dom.grabar.textContent='■ Terminar grabación';dom.grabar.setAttribute('aria-pressed','true');aviso.textContent='Grabando solo el juego y su sonido. Pulsa Terminar grabación al acabar.';
   }catch(e){aviso.textContent='No se pudo iniciar la grabación. Inténtalo desde Chrome o Edge.';console.warn(e);}
 }
 dom.accion.addEventListener('click',accion);dom.pausa.addEventListener('click',pausar);
 dom.sonido.addEventListener('click',()=>{const activo=audio.alternar();dom.sonido.setAttribute('aria-pressed',String(activo));dom.sonido.innerHTML='♫ <span>Sonido '+(activo?'activado':'desactivado')+'</span>';});
 document.querySelector('#izquierda').addEventListener('click',e=>{e.preventDefault();moverCarril(-1);});
 document.querySelector('#derecha').addEventListener('click',e=>{e.preventDefault();moverCarril(1);});
 dom.grabar.addEventListener('click',grabar);
 /** Captura el lienzo real, con nombre y puntaje, para documentar ambos niveles sin editar imágenes. */
 document.querySelector('#captura').addEventListener('click',()=>{
   if(!game?.canvas)return;
   const a=document.querySelector('#descarga-captura');a.download=`Ruta03-Nivel-${partida.nivel}-${partida.estado}.png`;
   a.href=game.canvas.toDataURL('image/png');a.hidden=false;
 });
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&partida.estado==='jugando'){partida=R.pausar(partida);sincronizar(true);}});
 window.addEventListener('pagehide',()=>{audio.parar();if(grabador?.state==='recording')grabador.stop();});
 if(!window.Phaser){document.querySelector('#fallo').hidden=false;return;}
 game=new Phaser.Game(W,H,Phaser.CANVAS,'juego',{preload,create,update},false,true);
})();
