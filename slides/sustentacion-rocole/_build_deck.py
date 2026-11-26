# -*- coding: utf-8 -*-
"""Genera composition/index.html — rediseño infográfico editorial RoCoLe."""
from pathlib import Path
from escenas import CSS, build

OUT = Path(__file__).parent / "composition" / "index.html"

NOTES = {
    "s01": (
        "Gio\n\n"
        "Queríamos evaluar si el color y la textura de una fotografía permiten distinguir "
        "hojas sanas de hojas con alteraciones visibles. Para comprobarlo, cambiamos la "
        "manera de representar la imagen y medimos qué efecto tuvo en la clasificación."
    ),
    "s02": (
        "Gio\n\n"
        "Verificamos que los 1.560 archivos abrían y tenían etiquetas. Elegimos RoCoLe "
        "para mantener una misma especie, unas condiciones de captura y un esquema de "
        "anotación comparables. Todos los nombres eran distintos. Al comparar el contenido "
        "encontramos fotografías repetidas."
    ),
    "s03": (
        "Gio\n\n"
        "Los duplicados se identificaron comparando la huella digital del contenido: "
        "67 pares idénticos con nombres distintos. En 55 pares conservamos una copia. "
        "En los 15 de severidad, ambas ya coincidían en la clase binaria afectada; la "
        "decisión de nivel se documentó con revisión visual asistida por IA. En 12 pares "
        "apartamos ambas copias. Por eso 67 pares dieron 79 retiros. "
        "Después de retirar las copias exactas todavía quedaba otra relación importante: "
        "dos fotos diferentes podían mostrar la misma hoja."
    ),
    "s04": (
        "Víctor\n\n"
        "Si entrenábamos con el haz y evaluábamos con el envés, podíamos estar midiendo "
        "qué tan bien reconocía el modelo una hoja que ya conocía. Agrupamos por planta "
        "y unimos también los identificadores vinculados por duplicados exactos."
    ),
    "s05": (
        "Víctor\n\n"
        "ExG y NGRDI miden el predominio del verde de dos maneras. Para cada índice "
        "guardamos media y desviación estándar. Contamos qué tonos de gris aparecen "
        "juntos en píxeles vecinos: de ahí salieron contraste, homogeneidad y energía. "
        "VARI se retiró porque su denominador podía acercarse a cero."
    ),
    "s06": (
        "Víctor\n\n"
        "El 19 % corresponde a esta fotografía. El color se calculó sobre los píxeles "
        "de hoja. Para GLCM se usó el rectángulo que la contiene y se puso a cero el "
        "exterior, de modo que el borde aún puede influir en la textura. "
        "Una vez delimitada la hoja, quisimos saber qué información de color se perdía "
        "al quedarnos con un promedio."
    ),
    "s07": (
        "Camilo\n\n"
        "Dos hojas pueden tener un verde promedio parecido, aunque una contenga "
        "pequeñas zonas amarillas y la otra sea más uniforme. El histograma cuenta qué "
        "proporción de la hoja cae en cada rango. Hicimos el conteo por separado para "
        "matiz, saturación y brillo."
    ),
    "s08": (
        "Camilo\n\n"
        "Calculamos el F1 de cada clase a partir de su precisión y sensibilidad, y "
        "luego promediamos las dos clases con el mismo peso. En Random Forest el salto "
        "más grande fue de A a B. Consultamos esta partición durante el desarrollo, "
        "así que quisimos comprobar cuánto variaba el desempeño al cambiar las plantas "
        "evaluadas."
    ),
    "s09": (
        "Camilo\n\n"
        "D mantuvo las 23 características de C, utilizó las 1.481 imágenes y comparó "
        "tres modelos. Por eso el 0,74 de C y el resultado de D corresponden a "
        "protocolos distintos."
    ),
    "s10": (
        "Dora\n\n"
        "La logística aporta una referencia lineal. SVM permitió probar fronteras "
        "lineales y curvas. Random Forest combina árboles que pueden captar "
        "interacciones entre características. Elegimos el bosque por su mayor media "
        "observada. Los intervalos son aproximados."
    ),
    "s11": (
        "Dora\n\n"
        "La salida del modelo sigue siendo sana o afectada. Usamos la etiqueta original "
        "para revisar con más detalle sus errores. De los 149 falsos negativos del "
        "estudio, 109 correspondieron a roya nivel 1. Es posible que una alteración "
        "leve contribuya poco a las medidas globales. Como las anotaciones delimitan "
        "la hoja completa, no pudimos comprobar esa explicación midiendo el área de "
        "cada lesión."
    ),
    "s12": (
        "Dora\n\n"
        "Entregamos un inventario depurado y cuadernos que permiten rastrear la "
        "predicción de cada imagen. La combinación de máscara, color y textura dio el "
        "mejor resultado entre las configuraciones exploradas, y la roya leve "
        "concentró la mayoría de los falsos negativos. Para evaluar este flujo en "
        "campo habría que obtener la máscara de cada fotografía nueva y probarlo con "
        "plantas externas."
    ),
    "r1": "Respaldo · Espacio de búsqueda de hiperparámetros por modelo.",
    "r2": "Respaldo · Matriz Random Forest en D: [[605, 153], [149, 574]].",
    "r3": (
        "Respaldo · EDA: cobertura mediana 24,9 % del inventario "
        "(distinta del 19 % de la foto de ejemplo)."
    ),
}


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def scene(sid, start, duration, label, inner):
    return f'''
  <div id="{sid}" class="clip scene" data-start="{start}" data-duration="{duration}"
       data-label="{label}" data-track-index="1"
       style="position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;background:var(--bg)">
    <div id="{sid}-stage" class="stage">{inner}</div>
  </div>'''


html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<title>Sustentación RoCoLe</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{
  font-family: "Source Serif 4";
  font-weight: 400;
  src: url("assets/fonts/source-serif-4-latin-400-normal.woff2") format("woff2");
}}
@font-face {{
  font-family: "Source Serif 4";
  font-weight: 600;
  src: url("assets/fonts/source-serif-4-latin-600-normal.woff2") format("woff2");
}}
:root {{
  --bg: #FAF9F5;
  --ink: #202824;
  --green: #176B52;
  --teal: #31A99A;
  --gold: #E9B949;
  --terra: #C65732;
  --muted: #5A635E;
  --line: #D8D4CA;
  --font: "Poppins", system-ui, sans-serif;
  --serif: "Source Serif 4", "EB Garamond", Georgia, serif;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1920px; min-height: 1080px; background: var(--bg); color: var(--ink); font-family: var(--font); }}
.stage {{ position: absolute; inset: 0; padding: 64px 88px 56px; }}
.scene {{ z-index: 1; }}
.kicker {{ font-size: 22px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--green); margin-bottom: 14px; }}
.title {{ font-size: 54px; font-weight: 600; line-height: 1.12; letter-spacing: -.02em; max-width: 920px; }}
.title-sm {{ font-size: 44px; font-weight: 600; line-height: 1.15; letter-spacing: -.02em; max-width: 1400px; }}
.serif {{ font-family: var(--serif); font-size: 30px; color: var(--muted); line-height: 1.35; }}
.claim {{ font-size: 30px; color: var(--ink); line-height: 1.35; max-width: 820px; }}
.anno {{ font-size: 28px; color: var(--muted); line-height: 1.3; }}
.num {{ font-variant-numeric: tabular-nums; font-weight: 600; }}
.foot {{ position: absolute; left: 88px; right: 88px; bottom: 32px; font-size: 24px; color: var(--muted); display: flex; justify-content: space-between; }}
.photo {{ display: block; width: 100%; height: 100%; object-fit: contain; background: #EEEBE3; }}
.frame {{ border: 2px solid var(--ink); background: #EEEBE3; overflow: hidden; }}
.call {{ font-size: 28px; font-weight: 600; }}
.call.ok {{ color: var(--green); }}
.call.bad {{ color: var(--terra); }}
.arrow-curve {{ fill: none; stroke: var(--terra); stroke-width: 4; stroke-linecap: round; }}
.brace {{ stroke: var(--green); stroke-width: 3; fill: none; stroke-linecap: round; }}
.split-bar {{ display: flex; height: 56px; border-radius: 8px; overflow: hidden; width: 100%; max-width: 1100px; }}
.split-bar .a {{ background: var(--green); }}
.split-bar .b {{ background: var(--terra); }}
.branch {{ display: flex; gap: 48px; margin-top: 28px; }}
.branch .col {{ flex: 1; }}
.branch h3 {{ font-size: 30px; color: var(--green); margin-bottom: 12px; }}
.branch.bad h3 {{ color: var(--terra); }}
.branch p {{ font-size: 28px; line-height: 1.35; }}
.eq {{ font-size: 40px; font-weight: 600; margin-top: 28px; font-variant-numeric: tabular-nums; }}
.strip {{ display: flex; height: 72px; border-radius: 10px; overflow: hidden; margin-top: 24px; }}
.strip span {{ display: flex; align-items: center; justify-content: center; color: #fff; font-size: 26px; font-weight: 600; }}
.hsv-bars {{ display: flex; align-items: flex-end; gap: 10px; height: 280px; }}
.hsv-bars i {{ flex: 1; background: linear-gradient(180deg, var(--teal), var(--green)); border-radius: 6px 6px 0 0; min-width: 28px; }}
.ci-row {{ display: grid; grid-template-columns: 300px 1fr 200px; gap: 20px; align-items: center; margin: 22px 0; font-size: 30px; }}
.ci-track {{ position: relative; height: 10px; background: rgba(32,40,36,.08); border-radius: 5px; }}
.ci-range {{ position: absolute; top: 1px; height: 8px; border-radius: 4px; background: rgba(23,107,82,.35); }}
.ci-dot {{ position: absolute; top: 50%; width: 18px; height: 18px; border-radius: 50%; transform: translate(-50%,-50%); background: var(--green); border: 3px solid var(--bg); }}
.ci-row.best .ci-dot {{ background: var(--teal); }}
.ci-row.best .name {{ color: var(--green); font-weight: 600; }}
.folds {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-top: 24px; }}
.fold {{ min-height: 220px; border: 3px solid var(--line); border-radius: 12px; padding: 16px; background: #fff; }}
.fold .tag {{ font-size: 22px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }}
.fold.eval {{ border-color: var(--terra); background: rgba(198,87,50,.06); }}
.fold.eval .tag {{ color: var(--terra); }}
.fold.train {{ border-color: var(--green); }}
.inner {{ margin-top: 16px; display: flex; flex-direction: column; gap: 8px; opacity: 0; }}
.inner b {{ display: block; padding: 10px 12px; border-radius: 8px; font-size: 22px; font-weight: 500; background: rgba(23,107,82,.12); color: var(--green); }}
.inner b.sel {{ background: rgba(198,87,50,.14); color: var(--terra); }}
.flow {{ display: flex; align-items: center; gap: 18px; font-size: 28px; font-weight: 500; margin-top: 28px; flex-wrap: wrap; }}
.flow em {{ font-style: normal; padding: 10px 16px; border: 2px solid var(--ink); border-radius: 999px; }}
.names {{ margin-top: 36px; display: flex; gap: 36px; font-family: var(--serif); font-size: 30px; color: var(--muted); }}
.illo {{ position: absolute; pointer-events: none; }}
.plot-wrap {{ position: relative; height: 520px; margin-top: 12px; padding: 8px 24px 48px 72px; background: #fff; border: 2px solid var(--line); border-radius: 12px; overflow: hidden; }}
.plot-svg {{ width: 100%; height: 100%; overflow: hidden; display: block; }}
.legend {{ display: flex; gap: 28px; margin-top: 14px; font-size: 26px; }}
.mosaic-box {{ width: 720px; height: 720px; background: #fff; border: 2px solid var(--ink); overflow: hidden; }}
.mosaic-box img {{ width: 100%; height: 100%; object-fit: contain; object-position: center; display: block; }}
.fn-bar {{ display: flex; height: 48px; border-radius: 8px; overflow: hidden; max-width: 900px; margin-top: 20px; }}
.fn-bar .ok {{ background: var(--green); }}
.fn-bar .bad {{ background: var(--terra); }}
.matrix {{ display: grid; grid-template-columns: 160px 1fr 1fr; gap: 10px; max-width: 820px; font-size: 28px; }}
.matrix .c {{ background: #fff; border: 2px solid var(--line); border-radius: 10px; padding: 20px; text-align: center; }}
.matrix .big {{ font-size: 40px; font-weight: 600; }}
{CSS}
</style>
</head>
<body style="margin:0">
<script type="application/hyperframes-slideshow+json">
{{
  "slides": [
    {{ "sceneId": "root", "startTime": 0, "endTime": 30, "notes": "{esc(NOTES['s01'])}", "fragments": [8.0, 18.0] }},
    {{ "sceneId": "root", "startTime": 30, "endTime": 70, "notes": "{esc(NOTES['s02'])}", "fragments": [34.0, 52.0] }},
    {{ "sceneId": "root", "startTime": 70, "endTime": 130, "notes": "{esc(NOTES['s03'])}", "fragments": [76.0, 100.0] }},
    {{ "sceneId": "root", "startTime": 130, "endTime": 175, "notes": "{esc(NOTES['s04'])}", "fragments": [136.0, 158.0] }},
    {{ "sceneId": "root", "startTime": 175, "endTime": 225, "notes": "{esc(NOTES['s05'])}", "fragments": [181.0, 205.0] }},
    {{ "sceneId": "root", "startTime": 225, "endTime": 270, "notes": "{esc(NOTES['s06'])}", "fragments": [235.0, 255.0] }},
    {{ "sceneId": "root", "startTime": 270, "endTime": 310, "notes": "{esc(NOTES['s07'])}", "fragments": [276.0, 292.0] }},
    {{ "sceneId": "root", "startTime": 310, "endTime": 360, "notes": "{esc(NOTES['s08'])}", "fragments": [318.0, 340.0] }},
    {{ "sceneId": "root", "startTime": 360, "endTime": 405, "notes": "{esc(NOTES['s09'])}", "fragments": [366.0, 386.0] }},
    {{ "sceneId": "root", "startTime": 405, "endTime": 445, "notes": "{esc(NOTES['s10'])}" }},
    {{ "sceneId": "root", "startTime": 445, "endTime": 500, "notes": "{esc(NOTES['s11'])}", "fragments": [451.0, 475.0] }},
    {{ "sceneId": "root", "startTime": 500, "endTime": 540, "notes": "{esc(NOTES['s12'])}", "fragments": [506.0, 524.0],
      "hotspots": [{{ "id": "hs-respaldo", "label": "Respaldo para preguntas", "target": "respaldo", "region": {{ "x": 60, "y": 84, "w": 36, "h": 10 }} }}] }}
  ],
  "slideSequences": [{{
    "id": "respaldo",
    "label": "Respaldo para preguntas del profesor",
    "slides": [
      {{ "sceneId": "root", "startTime": 540, "endTime": 560, "notes": "{esc(NOTES['r1'])}" }},
      {{ "sceneId": "root", "startTime": 560, "endTime": 580, "notes": "{esc(NOTES['r2'])}" }},
      {{ "sceneId": "root", "startTime": 580, "endTime": 600, "notes": "{esc(NOTES['r3'])}" }}
    ]
  }}]
}}
</script>
<div id="root" data-composition-id="root" data-start="0" data-duration="600"
     data-width="1920" data-height="1080" data-label="Sustentación RoCoLe"
     style="position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--bg)">
'''

# Escenas principales y material de respaldo.
r1 = scene("r1", 540, 20, "R1 · Hiperparámetros", '''
  <div class="kicker">Respaldo R1</div>
  <h1 class="title-sm">Espacio de búsqueda de hiperparámetros</h1>
  <div style="margin-top:36px;font-size:30px;line-height:1.55;max-width:1400px">
    <p><strong style="color:var(--green)">Logística</strong> · C = 0,001 / 0,01 / 0,1 / 1 / 10 / 100</p>
    <p style="margin-top:18px"><strong style="color:var(--teal)">SVM</strong> · C = 0,1 / 1 / 10 · núcleos lineal o RBF</p>
    <p style="margin-top:18px"><strong style="color:var(--terra)">Random Forest</strong> · 100 / 200 / 400 árboles · profundidad 5 / 10 / 20 o sin límite</p>
    <p class="anno" style="margin-top:28px">La mejor configuración se elige en cada pliegue externo por el promedio interno de F1 macro.</p>
  </div>
  <div class="foot"><span>Fuera del video principal</span><span></span></div>
''')

r2 = scene("r2", 560, 20, "R2 · Matriz D", '''
  <div class="kicker">Respaldo R2</div>
  <h1 class="title-sm">Matriz completa de Random Forest en D</h1>
  <p class="anno" style="margin:16px 0">Filas = referencia · columnas = predicción</p>
  <div class="matrix">
    <div></div><div class="c anno">Pred. sana</div><div class="c anno">Pred. afectada</div>
    <div class="c anno">Ref. sana</div><div class="c big">605</div><div class="c big">153</div>
    <div class="c anno">Ref. afectada</div><div class="c big" style="color:var(--terra)">149</div><div class="c big" style="color:var(--green)">574</div>
  </div>
  <p class="anno" style="margin-top:24px">Exactitud (605+574)/1.481 = 79,6 % · Sensibilidad afectada 574/723 = 79,4 %</p>
  <div class="foot"><span>Fuera del video principal</span><span></span></div>
''')

r3 = scene("r3", 580, 20, "R3 · EDA", '''
  <div class="kicker">Respaldo R3</div>
  <h1 class="title-sm">EDA de imágenes y límites</h1>
  <div style="display:flex;gap:48px;margin-top:36px;font-size:36px">
    <div><span class="num" style="color:var(--green);font-size:56px">758</span><div class="anno">sanas</div></div>
    <div><span class="num" style="color:var(--terra);font-size:56px">155</span><div class="anno">ácaro</div></div>
    <div><span class="num" style="color:var(--terra);font-size:56px">568</span><div class="anno">roya</div></div>
  </div>
  <div style="margin-top:40px;font-size:30px;line-height:1.5;max-width:1400px">
    <p>Cobertura mediana de hoja en el inventario: <span class="num">24,9 %</span> (cuartiles 18,9 % y 31,8 %)</p>
    <p style="margin-top:12px">Distinta del <span class="num">19 %</span> de la fotografía de ejemplo C1P1H1</p>
    <p style="margin-top:12px">Brillo dentro de la máscara: mediana <span class="num">133</span> (cuartiles 117 y 151)</p>
  </div>
  <div class="foot"><span>Fuera del video principal</span><span></span></div>
''')

html += "\n".join([*build(scene), r1, r2, r3])

html += '''
</div>
<script>
  window.__timelines = window.__timelines || {};
  const IR = { immediateRender: false };
  const tl = gsap.timeline({ paused: true });

  const WINDOWS = [
    ["s01",0,30],["s02",30,70],["s03",70,130],["s04",130,175],
    ["s05",175,225],["s06",225,270],["s07",270,310],["s08",310,360],
    ["s09",360,405],["s10",405,445],["s11",445,500],["s12",500,540],
    ["r1",540,560],["r2",560,580],["r3",580,600]
  ];
  WINDOWS.forEach(([id]) => gsap.set("#"+id, { zIndex: 1 }));
  WINDOWS.forEach(([id, start, end]) => {
    tl.set("#"+id, { zIndex: 20 }, start);
    tl.set("#"+id, { zIndex: 1 }, end);
  });

  // Los ejemplos científicos se revelan sobre la misma fotografía.
  tl.to("#exg-reveal", {opacity:1, duration:0.65}, 197);
  tl.to("#mask-reveal", {opacity:1, duration:0.8}, 232);
  const reveals = [
    ["#s02 .pillfree", 40], ["#s03 .rust", 94],
    ["#s04 .footnote", 155], ["#s07 .caption", 280],
    ["#s08 .numlg", 330], ["#s10 .numlg", 418],
    ["#s11 figcaption", 459], ["#s12 .under", 515]
  ];
  reveals.forEach(([target, start]) => {
    tl.set(target, {opacity:0}, 0);
    tl.to(target, {opacity:1, duration:0.5}, start);
  });
  tl.to({}, { duration: 0.001 }, 599.999);
  tl.seek(0);
  window.__timelines["root"] = tl;
</script>
</body>
</html>
'''

OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
