/** Pruebas de comportamiento independiente del render: vidas, reglas de puntuación y cambio de nivel. */
const {test}=require('node:test');const a=require('node:assert/strict');const R=require('../public/reglas.js');
test('Comienza con tres vidas, cero puntos y primer nivel',()=>{a.deepEqual(R.empezar(),{estado:'jugando',nivel:1,puntos:0,vidas:3,invulnerable:0,tiempo:0});});
test('El tercer punto activa transición y no concede victoria',()=>{let s=R.empezar();for(let i=0;i<3;i++)s=R.puntuar(s);a.equal(s.estado,'transicion');a.equal(s.puntos,3);a.equal(s.nivel,1);});
test('La transición no permite seguir acumulando puntos',()=>{let s={...R.empezar(),estado:'transicion',puntos:3};a.equal(R.puntuar(s).puntos,3);});
test('El segundo nivel conserva puntos y vidas',()=>{let s=R.segundoNivel({...R.empezar(),estado:'transicion',puntos:3,vidas:2});a.equal(s.nivel,2);a.equal(s.vidas,2);a.equal(s.puntos,3);});
test('Se gana solo al sumar tres puntos adicionales en nivel dos',()=>{let s=R.segundoNivel({...R.empezar(),estado:'transicion',puntos:3});s=R.puntuar(s);s=R.puntuar(s);a.equal(s.estado,'jugando');s=R.puntuar(s);a.equal(s.estado,'ganaste');a.equal(s.puntos,6);});
test('Un choque resta exactamente una vida y no suma puntos',()=>{let s=R.chocar(R.empezar());a.equal(s.vidas,2);a.equal(s.puntos,0);});
test('Un mismo impacto no puede quitar dos vidas durante protección',()=>{let s=R.chocar(R.empezar());a.equal(R.chocar(s).vidas,2);});
test('Tres impactos separados producen derrota con cero vidas',()=>{let s=R.empezar();for(let i=0;i<3;i++){s=R.chocar(s);for(let j=0;j<30;j++)s=R.avanzar(s,.05);}a.equal(s.estado,'perdiste');a.equal(s.vidas,0);});
test('No se gana ni puntúa después de la derrota',()=>{let s={...R.empezar(),estado:'perdiste',vidas:0,puntos:2};a.equal(R.puntuar(s).puntos,2);});
test('Pausa conserva el tiempo y no admite choques ni puntos',()=>{let s=R.pausar({...R.empezar(),puntos:2,tiempo:8});s=R.avanzar(s,1);s=R.chocar(s);s=R.puntuar(s);a.equal(s.tiempo,8);a.equal(s.vidas,3);a.equal(s.puntos,2);});
test('Reanudar conserva estado de progreso',()=>{let s=R.reanudar(R.pausar({...R.empezar(),puntos:2,vidas:1}));a.equal(s.estado,'jugando');a.equal(s.vidas,1);a.equal(s.puntos,2);});
test('No se puede saltar a nivel dos desde la portada',()=>{a.equal(R.segundoNivel(R.nuevaPartida()).nivel,1);});
test('Segundo nivel realmente aumenta velocidad y cambia todos los obstáculos',()=>{a.ok(R.NIVELES[2].velocidad>R.NIVELES[1].velocidad);a.ok(R.NIVELES[2].intervalo<R.NIVELES[1].intervalo);a.equal(R.NIVELES[2].tipos.some(t=>R.NIVELES[1].tipos.includes(t)),false);});
test('Reintentar no hereda vidas ni puntaje anteriores',()=>{const anterior={...R.empezar(),estado:'perdiste',vidas:0,puntos:5,nivel:2};const nuevo=R.empezar();a.equal(nuevo.vidas,3);a.equal(nuevo.puntos,0);a.equal(nuevo.nivel,1);a.equal(anterior.puntos,5);});
