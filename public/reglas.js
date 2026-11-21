/** Reglas de Ruta 03. Módulo puro compartido por principal.js y las pruebas Node.
 * El motor Phaser detecta las colisiones; este módulo controla vidas, puntos y estados. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ReglasRuta = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const NIVELES = Object.freeze({
    1: Object.freeze({nombre: 'Costa al amanecer', velocidad: 230, intervalo: 2.15, meta: 3, tipos: ['rival', 'barril']}),
    2: Object.freeze({nombre: 'Ciudad de neón', velocidad: 355, intervalo: 1.55, meta: 6, tipos: ['camion', 'barrilRojo']})
  });
  /** Crea una partida nueva sin modificar sesiones anteriores. */
  function nuevaPartida() { return {estado: 'portada', nivel: 1, puntos: 0, vidas: 3, invulnerable: 0, tiempo: 0}; }
  /** Inicia desde cero; reintentar también restablece las tres vidas. */
  function empezar() { return {...nuevaPartida(), estado: 'jugando'}; }
  /** Solo el tiempo de juego reduce la protección; una pestaña oculta no consume la partida. */
  function avanzar(s, segundos) {
    if (s.estado !== 'jugando') return s;
    const dt = Math.max(0, Math.min(Number(segundos) || 0, .05));
    return {...s, tiempo: s.tiempo + dt, invulnerable: Math.max(0, s.invulnerable - dt)};
  }
  /** Cada obstáculo realmente esquivado vale un punto; los golpeados no puntúan. */
  function puntuar(s) {
    if (s.estado !== 'jugando') return s;
    const puntos = s.puntos + 1;
    if (s.nivel === 1 && puntos >= 3) return {...s, puntos: 3, estado: 'transicion'};
    if (s.nivel === 2 && puntos >= 6) return {...s, puntos: 6, estado: 'ganaste'};
    return {...s, puntos};
  }
  /** La protección impide perder varias vidas por el mismo choque o fotograma. */
  function chocar(s) {
    if (s.estado !== 'jugando' || s.invulnerable > 0) return s;
    const vidas = Math.max(0, s.vidas - 1);
    return {...s, vidas, invulnerable: 1.25, estado: vidas === 0 ? 'perdiste' : 'jugando'};
  }
  /** El segundo nivel conserva el puntaje y las vidas ganados en el primero. */
  function segundoNivel(s) {
    return s.estado === 'transicion' ? {...s, nivel: 2, estado: 'jugando', invulnerable: 1.25} : s;
  }
  /** Pausa reversible exclusiva del estado jugable. */
  function pausar(s) { return s.estado === 'jugando' ? {...s, estado: 'pausa'} : s; }
  /** Reanuda sin cambiar el tiempo, el puntaje o las vidas. */
  function reanudar(s) { return s.estado === 'pausa' ? {...s, estado: 'jugando'} : s; }
  return {NIVELES, nuevaPartida, empezar, avanzar, puntuar, chocar, segundoNivel, pausar, reanudar};
});
