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

## 2. Guion (`stories/<slug>/guion.py`, copia la estructura de `stories/payaso/guion.py`)
- `STYLE = "clasico"` (estilo «Tu IA te hizo rico»: protagonista de gorro naranja, colores planos, cámara suave).
- `TITLE`: 2 líneas, **sin «POV»**, con la palabra clave del miedo.
- Narración en segunda persona («tú»), con calma y detalle; cada detalle cuenta y se paga después.
- **Gancho en la primera frase** (empieza en el momento más fuerte), giros, cliffhanger al final de las partes 1 y 2.
- 3 partes de **80–90 s** cada una; partes 2+3 juntas ≤ 178 s (Short de YouTube).
- Última línea de cada parte: «¿Qué haces? Opción A: … Opción B: … Comenta A o B. Y sígueme, que la parte dos sale hoy / el final sale hoy / si quieres la segunda temporada, sígueme.»
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
