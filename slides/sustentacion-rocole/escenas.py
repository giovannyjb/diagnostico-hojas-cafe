"""Escenas de la sustentación. Las fotografías conservan el encuadre de RoCoLe."""
from html import escape

TIMES = [0, 30, 70, 130, 175, 225, 270, 310, 360, 405, 445, 500, 540]

CSS = """
.atlas {position:absolute;inset:0;padding:72px 96px 52px;display:flex;flex-direction:column;gap:22px;background:#fbfaf5;color:#18372e;font:34px/1.35 var(--font)}
.atlas h1,.atlas h2,.atlas h3,.atlas p,.atlas figure {margin:0}
.atlas h2 {font-size:64px;letter-spacing:-.035em;line-height:1.08;font-weight:650;max-width:1620px}
.atlas h1 {font-size:88px;line-height:1.035;letter-spacing:-.045em;font-weight:650}
#s01 .main .narrow {flex:1.05} #s01 .main .wide {flex:1.2} #s01 h1 {font-size:75px;text-wrap:balance} .atlas .ey {font-size:24px;font-weight:650;color:#386655;letter-spacing:.085em;text-transform:uppercase}
.atlas .main {display:flex;flex:1;min-height:0;align-items:center;gap:72px}
.atlas .col {flex:1;min-width:0}
.atlas .wide {flex:1.36}
.atlas .narrow {flex:.82}
.atlas .copy {font-family:var(--serif);font-size:43px;line-height:1.24;color:#344d43}
.atlas .body {font-size:34px;line-height:1.4;color:#344d43}
.atlas .numlg {font-size:104px;letter-spacing:-.065em;font-weight:650;line-height:1.05;color:#166047}
.atlas .stat {font-weight:650;font-size:54px;line-height:1.12;color:#166047}
.atlas .rust {color:#a34430}
.atlas .under {border-top:2px solid #cdd7cb;padding-top:22px;margin-top:26px}
.atlas .small {font-size:27px;color:#41584e;line-height:1.3}
.atlas .footnote {border-top:2px solid #cdd7cb;padding-top:16px;font-size:25px;color:#40584c;display:flex;align-items:center;min-height:56px}
.atlas img {display:block;width:100%;height:auto;max-height:590px;object-fit:contain}
.atlas .art {max-height:670px}
.atlas .photo-real {width:100%;height:auto}
.atlas figcaption {margin-top:12px;color:#395348;font-size:28px}
.atlas .pair {display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:start}
.atlas .plantlayout {display:grid;grid-template-columns:1fr .8fr 1fr;gap:48px;align-items:center;flex:1;min-height:0}
.atlas .plantlayout figure img {width:100%;max-height:228px}
.atlas .plantlayout figure+figure {margin-top:12px}
.atlas .plantlayout figcaption {font-size:23px;margin-top:3px}
.atlas .plantlayout .art {max-height:540px}
.atlas .band {display:flex;height:25px;overflow:hidden;margin:18px 0}
.atlas .band i {height:100%}
.atlas .statline {display:flex;align-items:baseline;gap:22px;margin:24px 0}
.atlas .statline b {min-width:125px;font-size:62px;line-height:1.02;color:#166047}
.atlas .statline span {font-size:36px}
.atlas .stack {display:grid;align-items:center}
.atlas .stack>* {grid-area:1 / 1}
.atlas .caption {font-size:27px;color:#43594e;margin-top:18px}
#s08 .main .wide,#s10 .main .wide {flex:2.5} #s08 .main .narrow,#s10 .main .narrow {flex:.85} .atlas .chart {width:100%;height:auto;display:block;max-height:675px;overflow:visible}
.atlas text {font-family:var(--font);fill:#213e33}
.atlas .foldmap {display:grid;grid-template-columns:165px repeat(5,1fr);gap:11px;align-items:center}
.atlas .foldmap .unit {height:54px;background:#a9c9ae;border-radius:2px}
.atlas .foldmap .out {background:#a64b36}
.atlas .foldmap .lab {font-size:24px}
.atlas .mini {font-size:25px;line-height:1.3}
.atlas .pillfree {display:flex;gap:40px;justify-content:space-between}
.atlas .pillfree b {display:block;font-size:45px}
.atlas .errors {flex-direction:column;align-items:stretch;justify-content:center;gap:28px}
.atlas .errors .pair {gap:48px}
.atlas .errors .pair img {max-height:480px}
.atlas .errors figcaption {font-size:32px}
.atlas .sp {margin-top:26px}
"""

def image(file, label, art=False):
    folder = "illustrations" if art else "figuras"
    return f'<img class="{"art" if art else "photo-real"}" src="assets/{folder}/{file}" alt="{escape(label)}">'

def fig(file, label):
    return f'<figure>{image(file,label)}<figcaption>{label}</figcaption></figure>'

def cols(left, right, first="col wide", second="col"):
    return f'<div class="main"><div class="{first}">{left}</div><div class="{second}">{right}</div></div>'

def bar(values, colors):
    return '<div class="band">' + ''.join(f'<i style="flex:{v};background:{c}"></i>' for v,c in zip(values,colors))+'</div>'

def txt(x,y,value,size=26,color="#213e33",anchor="start",bold=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{650 if bold else 400}" style="fill:{color}">{escape(value)}</text>'

def svg(w,h,items,label):
    return f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + ''.join(items)+'</svg>'

def rule(x,y,x2,y2,color="#c4d2c6",width=2):
    return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" />'

def dot(x,y,r,c):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def hist():
    # C1P1H1.jpg, data/featured/rocole/hsv_hist_features_masked.csv
    vals=[.0179761,1.1176259,94.4385017,4.4258963,0,0,0,0]
    items=[txt(8,30,"Porcentaje de píxeles de la hoja",26)]
    for v in [0,50,100]:
        y=340-v*2.55
        items.extend([rule(72,y,766,y),txt(60,y+7,str(v),23,anchor="end")])
    for i,v in enumerate(vals):
        x=85+i*84
        items.append(f'<rect x="{x}" y="{340-v*2.55}" width="61" height="{v*2.55}" fill="{("#19664e" if i==2 else "#9ebba6")}"/>')
        items.append(txt(x+30,382,str(i+1),23,anchor="middle"))
    items+=[txt(454,422,"Intervalo de matiz",25,anchor="middle")]
    return svg(795,440,items,"Histograma de matiz medido para C1P1H1")

def plot_abc():
    items=[]; pos=lambda v:170+(v-.30)*2300
    for v in [.34,.50,.60,.70,.80]:
        x=pos(v);items+=[rule(x,55,x,372),txt(x,415,f'{v:.2f}'.replace('.',','),24,anchor="middle")]
    for i,(lab,a,b) in enumerate([("Foto completa",.5617,.5707),("Con máscara",.6062,.6769),("Máscara e HSV",.6767,.7421)]):
        y=95+i*125
        items+=[txt(6,y+8,lab,23),rule(pos(a),y,pos(b),y,"#7d9d88",5),dot(pos(a),y,10,"#5c736f"),dot(pos(b),y,12,"#14664d"),txt(pos(a),y+44,f'{a:.2f}'.replace('.',','),25,"#435c57","middle"),txt(pos(b),y-22,f'{b:.2f}'.replace('.',','),27,"#14664d","middle",True)]
    items.extend([dot(260,486,9,"#5c736f"),txt(280,495,"Regresión logística",24),dot(700,486,10,"#14664d"),txt(720,495,"Random Forest",24)])
    return svg(1400,520,items,"F1 macro de los dos modelos en tres representaciones")

def plot_d():
    items=[]; pos=lambda v:285+(v-.71)*7000
    for v in [.72,.74,.76,.78,.80,.82]:
        x=pos(v);items+=[rule(x,28,x,320),txt(x,367,f'{v:.2f}'.replace('.',','),23,anchor="middle")]
    for i,(name,mid,lo,hi) in enumerate([("Regresión logística",.741,.725,.757),("SVM",.767,.719,.816),("Random Forest",.796,.778,.814)]):
        y=72+i*99;c="#166047" if i==2 else "#63796b"
        items+=[txt(0,y+10,name,26,c,bold=i==2),rule(pos(lo),y,pos(hi),y,c,5),rule(pos(lo),y-12,pos(lo),y+12,c),rule(pos(hi),y-12,pos(hi),y+12,c),dot(pos(mid),y,12,c),txt(1120,y+10,f'{mid:.3f}'.replace('.',','),30,c,bold=True)]
    return svg(1240,397,items,"F1 macro medio e intervalo aproximado del 95 % por modelo")

def foldmap():
    out=['<div class="foldmap"><span></span>']
    out += [f'<span class="lab">Pliegue {n+1}</span>' for n in range(5)]
    for i in range(5):
        out.append(f'<span class="lab">Vuelta {i+1}</span>')
        out.extend(f'<span class="unit {"out" if j==i else ""}"></span>' for j in range(5))
    return ''.join(out)+'</div>'

def build(scene):
    slides=[]
    def add(k,title,body,foot):
        i=len(slides)
        content=f'<article class="atlas"><div class="ey">{k}</div><h2>{title}</h2>{body}<div class="footnote">{foot}</div></article>'
        slides.append(scene(f's{i+1:02}',TIMES[i],TIMES[i+1]-TIMES[i],title,content))
    slides.append(scene("s01",0,30,"Portada",'<article class="atlas"><div class="ey">Proyecto Café</div>'+cols('<h1>Clasificación de alteraciones visibles en hojas de café</h1><p class="copy sp">Evaluamos si el color y la textura permiten distinguir hojas sanas y afectadas en fotografías de RoCoLe.</p>',image("captura-cafe.webp","Ilustración de una investigadora fotografiando un cafeto",True),"col narrow","col wide")+'<div class="footnote">Gio, Víctor, Camilo y Dora</div></article>'))
    add("Inventario original","RoCoLe reúne 1.560 fotografías de hojas de café",
        cols('<div class="pair">'+fig("C1P1H1.jpg","Hoja sana")+fig("C1P1H2.jpg","Hoja afectada")+'</div>'+bar([791,769],["#166047","#ae583c"])+'<div class="pillfree"><span><b>791</b>imágenes sanas</span><span><b>769</b>imágenes afectadas</span></div>',
             '<p class="copy">Las dos clases están casi equilibradas.</p><p class="body under">La clase afectada reúne casos de ácaro rojo y cuatro niveles de roya.</p>'),
        "Verificamos que todas las fotografías se podían abrir y tenían etiquetas completas.")
    add("Depuración","Encontramos 67 pares de fotografías idénticas",
        cols('<div class="pair">'+fig("C2P1H1.jpg","C2P1H1.jpg")+fig("C3P2H2.jpg","C3P2H2.jpg")+'</div><p class="caption">Dos archivos del inventario original contienen la misma fotografía.</p>',
             '<p class="stat">En 55 pares</p><p class="body">Conservamos una copia. En 15 de esos pares revisamos primero la severidad de la roya.</p><p class="stat rust under">En 12 pares</p><p class="body">Apartamos ambas copias porque las etiquetas discrepaban sobre el tipo de alteración o el estado de la hoja.</p>'),
        "Retiramos 79 archivos del inventario experimental. Quedaron 1.481 fotografías.")
    add("Partición por planta","Las dos caras de cada hoja quedaron juntas",
        '<div class="plantlayout"><div>'+fig("C1P1H1.jpg","Haz de la primera hoja")+fig("C1P1E1.jpg","Envés de la primera hoja")+'</div><div>'+image("cafeto.webp","Ilustración de un cafeto",True)+'<p class="caption" style="text-align:center">Planta C1P1</p></div><div>'+fig("C1P1H2.jpg","Haz de la segunda hoja")+fig("C1P1E2.jpg","Envés de la segunda hoja")+'</div></div>',
        "Los 357 grupos quedaron separados. Usamos 1.037 fotografías para entrenar, 218 para validar y 226 para probar.")
    add("Experimento A","Medimos el color y la textura de la imagen completa",
        cols('<div class="stack">'+image("C1P1H1.jpg","Fotografía completa de C1P1H1")+'<div id="exg-reveal" style="opacity:0;background:#fbfaf5">'+image("rocole_sample_exg_map.png","Mapa ExG de la misma fotografía")+'</div></div>',
             '<p class="copy">El índice de verde también responde a las hojas del fondo.</p><p class="body under">Resumimos el color con ExG y NGRDI. Para la textura medimos el contraste, la homogeneidad y la energía de los tonos de gris vecinos.</p>'),
        "Conservamos siete características. Excluimos VARI porque producía valores extremos.")
    add("Experimento B","La hoja ocupa el 19 % de esta fotografía",
        cols('<div class="stack">'+image("C1P1H1.jpg","Fotografía original de C1P1H1")+'<div id="mask-reveal" style="opacity:0">'+image("C1P1H1-mascara.jpg","La misma fotografía con el contorno anotado en RoCoLe")+'</div></div>',
             '<p class="copy">Al delimitar la hoja, cambió la medida del verde.</p><div class="statline"><b>0,26</b><span>en la foto completa</span></div><div class="statline"><b>0,47</b><span>dentro de la hoja</span></div><p class="small">Media del índice ExG en C1P1H1.</p>'),
        "Repetimos la evaluación con las mismas siete características y la misma partición.")
    add("Experimento C","El histograma conserva cómo se distribuye el color",
        cols(image("C1P1H1-mascara.jpg","Hoja delimitada para calcular el histograma")+'<p class="caption">En esta hoja, el 94,4 % de los píxeles cae en el tercer intervalo de matiz.</p>',hist(),"col","col wide"),
        "Medimos ocho rangos de matiz, cuatro de saturación y cuatro de brillo. El modelo recibió 23 características.")
    add("Resultados exploratorios","Ambos modelos mejoraron al delimitar la hoja y agregar HSV",
        cols(plot_abc(),'<p class="numlg">0,74</p><p class="copy">F1 macro de Random Forest con máscara e histogramas de color.</p><p class="small under">El clasificador de mayoría obtuvo 0,34.</p>',"col wide","col narrow"),
        "Comparamos las tres representaciones en las mismas 226 imágenes de prueba.")
    add("Experimento D","Evaluamos cada modelo con grupos de plantas que no había visto",
        cols(foldmap()+'<p class="caption">En cada vuelta, el pliegue terracota quedó reservado para la evaluación.</p>',
             '<p class="copy">Cinco pliegues para evaluar.</p><p class="body under">Dentro del entrenamiento, tres pliegues sirvieron para escoger los hiperparámetros. Cada grupo se evaluó una sola vez.</p>'),
        "Mantuvimos las 23 características del experimento C y evaluamos las 1.481 fotografías.")
    add("Comparación de modelos","Random Forest obtuvo el mayor F1 macro medio",
        cols(plot_d(),'<p class="numlg">0,796</p><p class="copy">Media en los cinco pliegues externos.</p><p class="small under">El intervalo aproximado del 95 % para Random Forest fue de 0,778 a 0,814.</p>',"col wide","col narrow"),
        "Los segmentos muestran intervalos aproximados del 95 %. El punto indica la media de cada modelo.")
    add("Análisis de errores","Una de cada tres imágenes con roya leve se clasificó como sana",
        '<div class="main errors"><div class="pair">'+fig("C1P29H2.jpg","El modelo la clasificó como afectada.")+fig("C2P18H1.jpg","El modelo la clasificó como sana.")+'</div><p class="body">Las dos fotografías tenían la misma etiqueta de referencia, roya nivel 1.</p></div>',
        "Random Forest detectó 224 de las 333 imágenes con roya leve. Las otras 109 se clasificaron como sanas.")
    add("Conclusiones","La principal dificultad fue detectar la roya leve",
        cols(image("analisis.webp","Ilustración de revisión de una fotografía de café en un computador",True),
             '<p class="copy">En RoCoLe, Random Forest alcanzó un F1 macro medio de 0,796 con medidas de color y textura de la hoja delimitada.</p><p class="body under">Para evaluar su uso en campo, primero habría que obtener la máscara de cada hoja nueva y probar el modelo con plantas externas.</p>'),
        "Los cuadernos permiten consultar la etiqueta y la predicción de cada una de las 1.481 imágenes.")
    return slides
