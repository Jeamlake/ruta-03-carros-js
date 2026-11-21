/** Música y efectos originales de Ruta 03. Web Audio se desbloquea solo al pulsar Jugar.
 * Se relaciona con principal.js y ofrece una salida adicional para grabar el audio de la partida. */
class SonidoRuta {
  constructor(){this.activo=true;this.contexto=null;this.bucle=null;this.buffers={};this.nivel=1;}
  /** Carga y decodifica archivos locales; no depende de servicios ni CDNs externos. */
  async iniciar(){
    const AudioCtx=window.AudioContext||window.webkitAudioContext;
    if(!AudioCtx)return;
    if(!this.contexto){
      this.contexto=new AudioCtx();this.master=this.contexto.createGain();this.master.gain.value=this.activo?.55:0;
      this.master.connect(this.contexto.destination);this.salida=this.contexto.createMediaStreamDestination();this.master.connect(this.salida);
      this.carga=Promise.all(['musica1','musica2','choque-carro','choque-barril','punto','nivel'].map(async n=>{
        const r=await fetch(window.RUTA_RECURSOS?.[n]||'assets/audio/'+n+'.wav');if(!r.ok)throw new Error('No se pudo cargar '+n);
        this.buffers[n]=await this.contexto.decodeAudioData(await r.arrayBuffer());
      }));
    }
    await this.contexto.resume();await this.carga;
  }
  /** Alterna sonido sin cambiar el juego ni interrumpir la grabación. */
  alternar(){this.activo=!this.activo;if(this.master)this.master.gain.value=this.activo?.55:0;return this.activo;}
  /** Reemplaza el bucle al cambiar de nivel. */
  musica(nivel){this.parar();this.nivel=nivel;if(!this.contexto||!this.buffers['musica'+nivel])return;
    const s=this.contexto.createBufferSource();s.buffer=this.buffers['musica'+nivel];s.loop=true;s.connect(this.master);s.start();this.bucle=s;}
  /** Detiene únicamente la música, dejando terminar el efecto del choque o de victoria. */
  parar(){if(this.bucle){try{this.bucle.stop();}catch{}this.bucle=null;}}
  /** Reproduce un efecto corto predecodificado. */
  efecto(nombre){if(!this.contexto||!this.buffers[nombre])return;const s=this.contexto.createBufferSource();s.buffer=this.buffers[nombre];s.connect(this.master);s.start();}
}
