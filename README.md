# Ruta 03

Juego de carros de **José Eduardo Alvarado Mejía** para Diseño y Desarrollo de Juegos Interactivos I, sección 45350, UTP, 2026-II.

Implementación en JavaScript con **Phaser CE 2.20.2**, basada en el enfoque `preload`, `create` y `update` de la guía de la semana 12. Usa Arcade Physics para las colisiones. Los gráficos y sonidos son originales del proyecto; no se incluyen sesiones, credenciales ni PDFs del docente.

## Jugar

Sitio: https://jeamlake.github.io/ruta-03-carros-js/

Para jugar sin servidor, abre `public/JUGAR-SIN-INSTALAR.html` en un navegador moderno. La copia autónoma contiene el mismo juego y sus recursos integrados. Los archivos separados de `public/` son la versión editable.

En la PC: `python servir.py` y visita http://127.0.0.1:8795/ . También puede abrirse `public/` con Live Server en VS Code.

## Reglas

- Flechas o W A S D para moverte. En celular puedes arrastrar el carro o cambiar de carril con los botones.
- Comienzas con tres vidas; cada colisión resta una. El objeto golpeado no suma puntos.
- Cada obstáculo que dejas atrás suma un punto. A los **3 puntos** termina el primer nivel y se habilita el segundo.
- El nivel 2 conserva las vidas y el puntaje; aumenta la velocidad de 230 a 355 píxeles por segundo y cambia los autos por camiones y los barriles naranjas por rojos.
- Completa **6 puntos acumulados**, tres por nivel, para ver **GANASTE**. Sin vidas aparece **VUELVE A INTENTARLO**.
- P o Escape pausa. Ocultar la pestaña también pausa. Reintentar restablece nivel, vidas y puntos.

## Recursos adicionales

Música original por nivel, sonidos diferentes para vehículos y barriles, efecto visual de impacto, protección de 1,25 segundos después del choque, pausa, controles accesibles, captura PNG y grabación de Canvas con audio. La grabación captura solo el juego: no usa micrófono, cámara ni la pantalla del usuario.

## Estructura

- `public/index.html` y `estilos.css`: interfaz y controles adaptables.
- `public/principal.js`: carga, escena Phaser, movimiento, obstáculos, colisiones, HUD y captura de evidencias.
- `public/reglas.js`: estados, vidas y puntaje sin depender del render.
- `public/sonido.js`: música, efectos y mezcla para grabar.
- `public/assets`: sprites SVG y sonidos WAV originales.
- `public/vendor`: Phaser CE y su licencia MIT.
- `public/entrega`: PDF, capturas y video de demostración.
- `tests/reglas.test.cjs`: pruebas automáticas de las reglas.
- `herramientas/crear_recursos.py`: genera los recursos originales.
- `herramientas/crear_portatil.py`: regenera el HTML autónomo.
- `.github/workflows/pages.yml`: prueba y publica `public/` en GitHub Pages al actualizar `main`.

## Comprobaciones

`node --test tests/reglas.test.cjs` comprueba vidas, protección, pausa, progresión exacta a tres puntos, victoria y reintento. La inspección de interfaz y el video complementan estas pruebas; no se promete una calificación específica.

## Relación con lo visto hasta la semana 15

Semana 2: presentación, controles y gameplay. Semana 9: GUI, entidades y HUD. Semana 12: Phaser, sprites y ciclo de vida. Semana 13: detección de colisiones 2D. Se mantiene JavaScript porque es lo que solicita la consigna, aunque las primeras sesiones también desarrollan proyectos en Unity.

## Licencias

Phaser CE conserva su licencia MIT en `public/vendor/PHASER-LICENSE.txt`. Los sprites y sonidos originales se generan con el código incluido. La entrega no copia los sprites de la imagen de referencia.
