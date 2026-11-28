# Playbook diario — «Historias varias» (solo terror)

Cuentas: TikTok @historias.varias82 · YouTube «Historias varias» · Instagram historias_varias_ia.
Cada día sale **1 historia de terror en 3 partes**. Todo es gratis: render local + Buffer.

## 0. Preparar la sesión
```bash
bash setup.sh     # librerías, voz Kokoro (GitHub releases) y fuentes
```

## 1. Elegir la historia (lo que esté en tendencia)
- Busca en la web qué historias de terror están virales **esta semana** en TikTok (#historiasdeterror, #terror, #creepypasta)
  y en Reddit (r/nosleep, r/creepyencounters, r/LetsNotMeet, r/Glitch_in_the_Matrix, r/Thetruthishere).
  Elige un **tema o leyenda** que esté sonando (p. ej. imitadores, reglas, niñera, llamadas, cosas en la ventana…).
- Las publicaciones de Reddit tienen autor: **no copies ninguna**. Toma la premisa o la leyenda y escribe una versión
  propia, ambientada en Colombia, con giro final nuevo. Las leyendas populares (Llorona, Silbón, la niñera y el payaso…) son folclor.
- No repitas una historia que ya esté en `stories/`.

## 1b. Formato «Ruleta de leyendas» (el formato de la cuenta desde el 24-nov)
- Gira la ruleta DE VERDAD al azar: `python3 -c "import secrets;print(secrets.randbelow(8))"` → índice en `engine/leyendas.py` (LEYENDAS).
  Si sale una leyenda usada en las últimas 4 historias (mira `stories/*/guion.py`, campo RULETA), vuelve a girar.
- `guion.py` lleva `RULETA = {"scene": "<primera escena>", "start": 0.4, "dur": 6.2, "target": <índice>}` y
  `TITLE = ("Ruleta de leyendas de miedo:", "la que salga, te la cuento")`.
- Parte 1: primera línea «Gira la ruleta de leyendas. La que salga, te cuento su historia. Y te advierto: ninguna termina bien.»
  (la escena dibuja `L.ruleta(...)`, ver `stories/tunda/panels.py`), segunda línea el nombre de la leyenda con la cara grande (`L.icono`).
- La historia es sobre ESA leyenda (versión propia, ambientada en Colombia, con detalles reales de la leyenda) y **termina en tragedia**.
- El monstruo debe dar MUCHO miedo: usa `L.icono(...)` para los primeros planos y crea su cuerpo entero en `engine/leyendas.py`
  (como `L.tunda`) si aún no existe. Final de la Parte 3: «Y sígueme, que la ruleta vuelve a girar.»

## 2. Guion (`stories/<slug>/guion.py`, copia la estructura de `stories/payaso/guion.py`)
- `STYLE = "clasico"` (estilo «Tu IA te hizo rico»: protagonista de gorro naranja, colores planos, cámara suave).
- `TITLE`: 2 líneas, **sin «POV»**, con la palabra clave del miedo.
- Narración en segunda persona («tú»), con calma y detalle; cada detalle cuenta y se paga después.
- **Gancho en la primera frase** (empieza en el momento más fuerte), giros, cliffhanger al final de las partes 1 y 2.
- 3 partes de **80–90 s** cada una; partes 2+3 juntas ≤ 178 s (Short de YouTube).
- Última línea de P1 y P2: «¿Qué haces? Opción A: … Opción B: … Comenta A o B. Y sígueme, que la parte dos sale hoy / el final sale hoy.»
- **FINAL CERRADO OBLIGATORIO (orden de Diego): NO hay segundas temporadas.** La Parte 3 resuelve TODO: qué le pasó al protagonista, al monstruo y a los secundarios; nada de cliffhanger ni «continuará». Prohibido escribir «segunda temporada», «2.ª temporada» o «parte 4» en guion o ENDCARD.
- Última línea de P3: «¿Y tú qué hubieras hecho? Opción A: … Opción B: … Comenta A o B. Y sígueme para más historias de terror.» (en ruleta: «Y sígueme, que la ruleta vuelve a girar.»). ENDCARD[3] = ("¿QUÉ HUBIERAS HECHO?", A, B, "SÍGUEME PARA MÁS TERROR").
- Voces: N narrador, M mamá/mujer, P papá/hombre mayor, K niño/niña, X voz ronca de monstruo, G voz «gemela» del protagonista.
- Llena `KEY`, `ENDCARD`, `FX` (flash/shake/red), `CUES` (boom, boom_s, heart, ping, pop, creak, knock3, steps, paper, whisper, doorbell, scrape, lock, riser_end), `MUSIC` (tense/dark/piano).

## 3. Escenas (`stories/<slug>/panels.py`, mira `stories/payaso/panels.py`)
- Personajes con `bust(...)` (el estilo «que enamore» se activa solo con STYLE clásico).
- **Monstruos con `engine/monstruos.py`**: `payaso_malo`, `imitadora`, `sombra`, `cara_ventana` — o crea uno nuevo en ese archivo
  siguiendo las mismas reglas: cuencas negras con pupila que brilla, sonrisa con dientes afilados, piel agrietada, tic nervioso.
- Escenarios reutilizables en `engine/scenes.py`. Los carteles (`tag2`) van en y ≥ 340 para no tapar los subtítulos.
- `python3 engine/check.py stories/<slug>` debe decir «ninguna» en los dos renglones.

## 4. Voz, cuadros de prueba y render
```bash
for p in 1 2 3; do python3 engine/tts.py stories/<slug> $p; done
python3 engine/render.py stories/<slug> 1 stills a01+2 a05+3 ...   # mira los PNG antes de renderizar
timeout 560 python3 engine/render.py stories/<slug> <parte> render 2   # si se corta, vuelve a correrlo: retoma lo que falte
bash engine/final.sh stories/<slug> <parte> videos/<fecha>/<slug>_p<parte>.mp4
# YouTube: une partes 2 y 3 con concat -c copy -> videos/<fecha>/<slug>_p2y3_youtube.mp4 (≤ 178 s)
```
Revisa cuadros del video final (ffmpeg -ss … -frames:v 1) antes de publicar.

## 5. Publicar con Buffer (organización «My organization», zona America/Bogota)
Sube los mp4 al repo (`git push`) y comprueba que `https://raw.githubusercontent.com/DiegoAndresMtz/historias-ia/main/videos/<fecha>/<archivo>` responde 200.

| Canal | ID | metadata |
|---|---|---|
| TikTok | 6b021bd8ece6dfde5f4c2a7d | `{"tiktok": {"isAiGenerated": false}}` |
| Instagram | 6b022370ece6dfde5f4c88a0 | `{"instagram": {"type": "reel", "shouldShareToFeed": true, "isAiGenerated": false}}` |
| YouTube | 6b021b7cece6dfde5f4c2751 | `{"youtube": {"title": "...", "categoryId": "1", "isAiGenerated": false, "privacy": "public", "madeForKids": false}}` |

Horario (hora Colombia, `mode: customScheduled`, `schedulingType: automatic`):
- Lunes a viernes: Parte 1 12:30 p. m. · Parte 2 7:00 p. m. · Parte 3 9:30 p. m.
- Sábado y domingo: Parte 1 11:00 a. m. · Parte 2 7:00 p. m. · Parte 3 9:30 p. m.
- TikTok e Instagram: las 3 partes.
- YouTube: **un solo Short al día, a las 9:45 p. m.** (Buffer rechaza un tercer video de YouTube dentro de 24 horas y no acepta videos de más de 3 min).
  YouTube va intercalado: mira qué video de YouTube quedó programado el día anterior.
  · Si fue la **Parte 1** de una historia → ese día va el `_p2y3_youtube.mp4` de ESA misma historia (título «… (Partes 2 y 3 FINAL)»).
  · Si fue un final (o no hay nada) → ese día va la **Parte 1** de la historia nueva del día (texto: «Parte 1. El final sale mañana»).
  Así YouTube publica una historia completa cada 2 días; las historias intermedias solo salen en TikTok e Instagram.
- Descripción: gancho de 1 línea + «Parte N de 3. ¿A o B? 👇» + 5 hashtags (#historiasdeterror #terror #miedo + 1 del tema + #historiasvarias; en YouTube #shorts primero).
- El plan gratis de Buffer permite 10 publicaciones en cola por canal: no programes más de 2 días adelante.
- Nunca pidas ni uses contraseñas; solo Buffer.

## Animación sin flotar y con personalidad (orden de Diego, 25-nov)
- Nadie flota: todos los personajes tienen piernas y zapatos (povlib.legs). Si un personaje se mueve, el motor lo hace CAMINAR solo (rebote de pasos y zancadas); no hace falta nada extra, pero muévelos por el piso, nunca por el aire.
- Monstruos de cuerpo entero con los pies plantados (el tic mueve el torso, no los pies).
- Cámara clásica quieta (sin acercamiento lento): solo cortes y golpes en palabras clave.
- Personalidad automática: al hablar inclina la cabeza, asiente y sube las cejas; mira alrededor y parpadea a su ritmo; tiembla de miedo con mood "shock", "worry" o "scared".
- Dale a cada personaje un rasgo propio en su dict: glasses="#color" (abuelas, tías), freckles=True (niños), mustache=True, mole=True, pants="#color".
- SIN LETREROS EXTRA (orden de Diego): en la imagen solo van los subtítulos, el título de arriba y la tarjeta A/B final. tag2 está apagado (scenes.TAGS = False); no dibujes carteles de texto, cuéntalo con dibujos.
- Espíritus que lloran o gimen (La Llorona, etc.): usa la voz "L" (sollozo tembloroso + eco + voz fantasma) y el sonido "lamento" en CUES.
- Sonidos de leyendas en CUES: "piar"/"piar_grave" (Pollo Maligno), "silbido_cerca"/"silbido_lejos" (El Silbón: escala do-re-mi que sube), "huesos" (conteo de huesos), "ladrido", "aullido", "latigo", "grito".

## 1c. FORMATO ACTUAL (desde 28-nov, orden de Diego): «Brote zombi» — trend #1 de terror en TikTok (nov-2026)
Diego pidió dejar la ruleta y recrear lo más viral. El trend: historias de supervivencia a un brote zombi, animadas con
personajes de palitos, narradas en SEGUNDA PERSONA, en un lugar cotidiano y reconocible, avanzando por días
(«Día uno…»), y cada parte termina en una decisión A/B. El LUGAR es el gancho.
- Ejemplo completo: stories/zombi_super/ (guion.py + panels.py). Motor de dibujo: engine/palitos.py
  (stick, zombi, horda, cara_zombi, supermercado, reja, cuarto_frio, techo_vidrio, calle_noche, camion, moto, callejon).
- Lugar NUEVO en Colombia cada historia (no repetir): TransMilenio/bus articulado, conjunto residencial, colegio,
  hospital, centro comercial, finca, peaje, estadio, edificio de oficinas, avión, ferry, discoteca, iglesia, cárcel…
  Agrega a palitos.py los escenarios que falten.
- TITLE = ("Brote zombi en <ciudad>:", "<quedaste atrapado en …>"). Parte 1 = Día uno, Parte 2 = Día dos, Parte 3 = Día tres.
- GANCHO: la primera frase arranca con acción; el primer ataque pasa ANTES del segundo 4. Nada de presentaciones.
- Partes de 40–55 s (6–8 líneas). Voz N. Zombis que den miedo: primer plano con cara_zombi en el momento fuerte, growl en CUES.
- Personaje «tú» = gorra amarilla (cap="#f2c230"). 4–6 personajes con un rasgo cada uno.
- Final cerrado y trágico en el Día tres (sin segunda temporada). Última línea: «¿Tú …? Opción A … Opción B … Comenta A o B. Y sígueme para más historias de supervivencia.»
- Textos de Buffer: «Día N del brote zombi: …» + #zombies #historiasdeterror #apocalipsiszombie #terror #historiasvarias.

## 1d. MOTOR DE ANIMACIÓN ACTUAL (desde 28-nov, orden de Diego): Remotion + Open Peeps
Diego pidió animaciones de mejor calidad. Ya NO se usa engine/render.py (palitos/Cairo) para los videos: se anima con
Remotion (React, carpeta remo/) y personajes dibujados a mano de Open Peeps (react-peeps, ilustraciones CC0).
La voz, los efectos y la música siguen saliendo de Python (guion.py → tts.py → sfx.py).

Pasos para una historia nueva <slug> (3 partes):
1. `bash setup.sh` (instala también remo/node_modules). Chrome está en /usr/bin/google-chrome.
2. stories/<slug>/guion.py igual que siempre (PARTS, KEY, CUES, MUSIC, ENDCARD, TITLE). panels.py ya no hace falta.
3. Audio de cada parte: `bash engine/remo_audio.sh <slug> <N>` → remo/src/data/<slug>_pN.json + remo/public/<slug>_pN.m4a.
4. Escenas: crea remo/src/stories/<slug>.tsx copiando la estructura de remo/src/stories/zombi_super.tsx:
   - una función por escena (mismo id que en guion.py) que recibe {t, w}; w('palabra') = segundo en que se dice esa palabra.
   - export const <SLUG>: Record<number, Meta> = {1: {title, badge: 'DÍA 1', keys, audio: '<slug>_p1.m4a', tl: <json>, scenes, endcard}, 2: …, 3: …}
   - regístrala en remo/src/stories/index.ts.
   Piezas disponibles (remo/src/kit.tsx y sets.tsx):
   - Char: persona de cuerpo entero (pose, face, hair, skin, clothes, flip, walk, zombie). Poses de pie: ShirtPantsBW/WB, RestingBW/WB,
     WalkingBW/WB, PointingFingerBW/WB, CrossedArmsBW/WB, EasingBW/WB, BlazerPantsBW/WB, RoboDanceOutline (zombis); sentado: ClosedLegWB…
     Caras: Calm, Smile, Fear, ConcernedFear, Awe, Concerned, Serious, Suspicious, Driven, Rage, Angry, Tired, Solemn, EyesClosed, Explaining, Cute.
     Pelo: Short, ShortScratch, ShortMessy, Long, Bun, Buns, GrayBun, Bald, BaldTop, Afro, Medium, MediumStraight, HatHip, Beanie…
   - zombie: <Char zombie pose="RoboDanceOutline" …/> (piel verdosa, ojos rojos, dientes, tirones). ZombieCloseup = primer plano que asusta.
   - Camera (zoom suave a palabras clave + sacudón), Flash, Vignette; escenarios: Market, Counter, Gate, ColdRoom, Skylight, Night, BackLot,
     Parking, Alley, Truck, Moto. Agrega escenarios nuevos a sets.tsx cuando el lugar lo pida (SVG 1080x1920, piso en FLOOR=1500).
   - La tarjeta A/B, el título, los subtítulos (3 palabras, KEY en amarillo), el grano y el audio los pone Episode solo.
5. MIRA cuadros antes del render: `cd remo && npx remotion still src/index.ts <slug-con-guiones>-p1 /tmp/x.png --frame=120 --browser-executable=/usr/bin/google-chrome`.
   Revisa que se vean los personajes, que nada quede negro y que el susto se vea.
6. Render: `bash engine/remo_render.sh <slug> <N> videos/<fecha>/<slug>_pN.mp4` (≈9–12 min por parte; córrelo en segundo plano y espera).
   El script recomprime al final (~7 Mbps): sin eso salen archivos de 70–100 MB que GitHub rechaza.
   Historias hechas con este motor: zombi_super (supermercado), zombi_transmi (TransMilenio).
7. YouTube (partes 2 y 3 juntas): `ffmpeg -f concat -safe 0 -i lista.txt -c copy videos/<fecha>/<slug>_p2y3_youtube.mp4`.
