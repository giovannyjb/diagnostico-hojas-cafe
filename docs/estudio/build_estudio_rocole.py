"""Guía de estudio en PDF: experimentos RoCoLe (A foto, B máscara, C HSV).

Los números salen de las matrices de test guardadas en los cuadernos 04
y de las tablas de validación en experiments/results/rocole/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
OUT_PDF = ROOT / "docs" / "estudio-rocole-baselines.pdf"
FIG_DIR = Path(__file__).resolve().parent / "figuras"

GREEN = "#1B4332"
LEAF = "#2D6A4F"
SAGE = "#D8F3DC"
CREAM = "#FBF8F3"
INK = "#1C1917"
MUTED = "#57534E"
LINE = "#E7E5E4"
RUST = "#9B2226"
AMBER = "#BC6C25"
GOLD = "#E9C46A"
BLUE = "#1D4E89"
SOFT = "#F4F1EA"

FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_I = r"C:\Windows\Fonts\segoeuii.ttf"
FONT_L = r"C:\Windows\Fonts\segoeuil.ttf"

# Matrices de test: filas = real (healthy, unhealthy), columnas = predicho.
PROTOCOLS = [
    {
        "key": "A",
        "name": "Foto completa",
        "short": "7 medidas, hoja + fondo",
        "log_cm": np.array([[61, 54], [45, 66]]),
        "rf_cm": np.array([[63, 52], [45, 66]]),
        "log_f1_test": 0.562,
        "rf_f1_test": 0.571,
        "maj_val": 0.341,
        "log_val": 0.617,
        "rf_val": 0.649,
        "log_C": "0.1",
        "rf_trees": "100",
        "rf_depth": "10",
    },
    {
        "key": "B",
        "name": "Máscara COCO",
        "short": "las mismas 7, solo la hoja",
        "log_cm": np.array([[69, 46], [43, 68]]),
        "rf_cm": np.array([[78, 37], [36, 75]]),
        "log_f1_test": 0.606,
        "rf_f1_test": 0.677,
        "maj_val": 0.341,
        "log_val": 0.716,
        "rf_val": 0.743,
        "log_C": "0.1",
        "rf_trees": "200",
        "rf_depth": "10",
    },
    {
        "key": "C",
        "name": "Máscara + HSV",
        "short": "7 + 16 bins de color",
        "log_cm": np.array([[80, 35], [38, 73]]),
        "rf_cm": np.array([[92, 23], [35, 76]]),
        "log_f1_test": 0.677,
        "rf_f1_test": 0.742,
        "maj_val": 0.341,
        "log_val": 0.798,
        "rf_val": 0.835,
        "log_C": "0.1",
        "rf_trees": "100",
        "rf_depth": "sin tope",
    },
]


def cm_stats(cm: np.ndarray) -> dict:
    healthy_ok, healthy_as_sick = int(cm[0, 0]), int(cm[0, 1])
    sick_as_healthy, sick_ok = int(cm[1, 0]), int(cm[1, 1])
    n = int(cm.sum())
    n_healthy = healthy_ok + healthy_as_sick
    n_sick = sick_as_healthy + sick_ok
    accuracy = (healthy_ok + sick_ok) / n
    recall_h = healthy_ok / n_healthy
    recall_u = sick_ok / n_sick
    prec_h = healthy_ok / (healthy_ok + sick_as_healthy)
    prec_u = sick_ok / (sick_ok + healthy_as_sick)
    f1_h = 2 * prec_h * recall_h / (prec_h + recall_h)
    f1_u = 2 * prec_u * recall_u / (prec_u + recall_u)
    f1_macro = (f1_h + f1_u) / 2
    col_h = healthy_ok + sick_as_healthy
    col_u = healthy_as_sick + sick_ok
    pe = (n_healthy * col_h + n_sick * col_u) / (n * n)
    kappa = (accuracy - pe) / (1 - pe)
    return {
        "n": n,
        "accuracy": accuracy,
        "recall_h": recall_h,
        "recall_u": recall_u,
        "prec_h": prec_h,
        "prec_u": prec_u,
        "f1_macro": f1_macro,
        "kappa": kappa,
        "missed_sick": sick_as_healthy,
        "extra_spray": healthy_as_sick,
        "caught_sick": sick_ok,
        "true_healthy": healthy_ok,
    }


def setup_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Segoe", FONT))
    pdfmetrics.registerFont(TTFont("Segoe-Bold", FONT_B))
    pdfmetrics.registerFont(TTFont("Segoe-Italic", FONT_I))
    pdfmetrics.registerFont(TTFont("Segoe-Light", FONT_L))


def styles() -> dict:
    s = {}
    s["h1"] = ParagraphStyle(
        "h1",
        fontName="Segoe-Bold",
        fontSize=16,
        leading=20,
        textColor=HexColor(GREEN),
        spaceAfter=4,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        fontName="Segoe-Bold",
        fontSize=12,
        leading=15,
        textColor=HexColor(INK),
        spaceBefore=8,
        spaceAfter=3,
    )
    s["body"] = ParagraphStyle(
        "body",
        fontName="Segoe",
        fontSize=10,
        leading=14,
        textColor=HexColor(INK),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    s["small"] = ParagraphStyle(
        "small",
        fontName="Segoe",
        fontSize=8.5,
        leading=11.5,
        textColor=HexColor(MUTED),
        spaceAfter=4,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Segoe",
        fontSize=10,
        leading=13.5,
        textColor=HexColor(INK),
        leftIndent=2,
    )
    s["callout"] = ParagraphStyle(
        "callout",
        fontName="Segoe",
        fontSize=9.5,
        leading=13,
        textColor=HexColor(INK),
    )
    s["callout_title"] = ParagraphStyle(
        "callout_title",
        fontName="Segoe-Bold",
        fontSize=9,
        leading=12,
        textColor=HexColor(GREEN),
        spaceAfter=2,
    )
    s["th"] = ParagraphStyle(
        "th",
        fontName="Segoe-Bold",
        fontSize=8,
        leading=10,
        textColor=white,
    )
    s["td"] = ParagraphStyle(
        "td",
        fontName="Segoe",
        fontSize=8,
        leading=10.5,
        textColor=HexColor(INK),
    )
    s["td_b"] = ParagraphStyle(
        "td_b",
        fontName="Segoe-Bold",
        fontSize=8,
        leading=10.5,
        textColor=HexColor(INK),
    )
    s["formula"] = ParagraphStyle(
        "formula",
        fontName="Segoe-Bold",
        fontSize=11,
        leading=15,
        textColor=HexColor(GREEN),
        alignment=TA_LEFT,
        spaceBefore=2,
        spaceAfter=4,
    )
    s["slide_title"] = ParagraphStyle(
        "slide_title",
        fontName="Segoe-Bold",
        fontSize=10,
        leading=13,
        textColor=HexColor(GREEN),
    )
    s["slide_body"] = ParagraphStyle(
        "slide_body",
        fontName="Segoe",
        fontSize=9,
        leading=12,
        textColor=HexColor(INK),
    )
    return s


S = None  # filled in main


def P(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, S[style])


def rule() -> HRFlowable:
    return HRFlowable(width="100%", thickness=1, color=HexColor(SAGE), spaceAfter=8, spaceBefore=1)


def callout(title: str, text: str, border: str = GREEN, bg: str = SAGE) -> Table:
    inner = [P(title, "callout_title"), P(text, "callout")]
    data = [[inner]]
    table = Table(data, colWidths=[174 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor(bg)),
                ("LINEBEFORE", (0, 0), (0, -1), 3.5, HexColor(border)),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def bullets(items: list[str]) -> ListFlowable:
    flow = [ListItem(P(item, "bullet"), leftIndent=8, bulletColor=HexColor(LEAF)) for item in items]
    return ListFlowable(flow, bulletType="bullet", start="•", leftIndent=12, bulletFontName="Segoe", bulletFontSize=9, spaceBefore=1, spaceAfter=6)


def section(title: str) -> list:
    return [P(title, "h1"), rule()]


def styled_table(header: list[str], rows: list[list[str]], col_widths: list[float]) -> Table:
    head = [P(cell, "th") for cell in header]
    body = []
    for row in rows:
        body.append([P(cell, "td_b" if i == 0 else "td") for i, cell in enumerate(row)])
    table = Table([head] + body, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Segoe-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor(LINE)),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor(CREAM)]),
    ]
    table.setStyle(TableStyle(style_cmds))
    return table


def save_fig(fig, name: str) -> Path:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_pipeline() -> Path:
    fig, ax = plt.subplots(figsize=(10.6, 2.15))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 2.15)
    ax.axis("off")
    boxes = [
        (0.15, "1.560 fotos", "RoCoLe crudo"),
        (2.25, "1.481 hojas", "curadas"),
        (4.35, "Split fijo", "train / val / test"),
        (6.45, "Medidas", "A · B · C"),
        (8.55, "Test 1 vez", "226 hojas"),
    ]
    for x, title, sub in boxes:
        patch = FancyBboxPatch(
            (x, 0.45),
            1.85,
            1.2,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=0,
            facecolor=GREEN,
        )
        ax.add_patch(patch)
        ax.text(x + 0.92, 1.18, title, ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        ax.text(x + 0.92, 0.78, sub, ha="center", va="center", color="#D8F3DC", fontsize=8)
    for x in (2.02, 4.12, 6.22, 8.32):
        ax.annotate("", xy=(x + 0.18, 1.05), xytext=(x, 1.05), arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.6))
    fig.tight_layout(pad=0.2)
    return save_fig(fig, "pipeline.png")


def fig_f1() -> Path:
    labels = [p["key"] + "  " + p["name"] for p in PROTOCOLS]
    x = np.arange(len(labels))
    width = 0.36
    val = [p["rf_val"] for p in PROTOCOLS]
    test = [p["rf_f1_test"] for p in PROTOCOLS]
    fig, ax = plt.subplots(figsize=(7.4, 3.55))
    bars_v = ax.bar(x - width / 2, val, width, label="Validación (elige el modelo)", color=GOLD, edgecolor="none")
    bars_t = ax.bar(x + width / 2, test, width, label="Prueba (se mira una vez)", color=GREEN, edgecolor="none")
    ax.axhline(0.34, color=RUST, lw=1, ls="--", label="Piso de mayoría en val (0.34)")
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("F1 macro del bosque")
    ax.set_xticks(x)
    ax.set_xticklabels(["A  foto completa", "B  máscara", "C  máscara + HSV"])
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color="#E7E5E4")
    for bars in (bars_v, bars_t):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02, f"{height:.2f}", ha="center", va="bottom", fontsize=8, color=INK)
    fig.tight_layout()
    return save_fig(fig, "f1_bosque.png")


def fig_confusions() -> Path:
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.5))
    for ax, proto in zip(axes, PROTOCOLS):
        cm = proto["rf_cm"]
        ax.imshow(cm, cmap="Blues", vmin=0, vmax=100)
        ax.set_xticks([0, 1], ["predicha sana", "predicha enferma"], fontsize=7.5)
        ax.set_yticks([0, 1], ["real sana", "real enferma"], fontsize=7.5)
        ax.set_title(f"{proto['key']}  {proto['name']}\nF1 macro {proto['rf_f1_test']:.2f}", fontsize=9, color=GREEN, pad=8)
        for (i, j), value in np.ndenumerate(cm):
            color = "white" if value >= 60 else INK
            ax.text(j, i, str(int(value)), ha="center", va="center", color=color, fontsize=13, fontweight="bold")
        ax.tick_params(length=0, pad=2)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.tight_layout(w_pad=2.4)
    return save_fig(fig, "confusiones_rf.png")


def fig_errors() -> Path:
    stats = cm_stats(PROTOCOLS[2]["rf_cm"])
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    names = ["Enfermas que se escapan\n(no se fumiga)", "Sanas fumigadas de más"]
    values = [stats["missed_sick"], stats["extra_spray"]]
    colors = [RUST, AMBER]
    bars = ax.barh(names, values, color=colors, height=0.62)
    ax.set_xlim(0, 50)
    ax.set_xlabel("Hojas en el test del bosque C (de 226)")
    for bar, value in zip(bars, values):
        ax.text(value + 0.8, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=11, fontweight="bold", color=INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    fig.tight_layout()
    return save_fig(fig, "errores_c.png")


def fig_glcm() -> Path:
    image = np.array(
        [
            [0, 0, 1, 1],
            [0, 2, 2, 1],
            [0, 2, 1, 1],
            [0, 0, 1, 1],
        ],
        dtype=int,
    )
    glcm = np.zeros((3, 3), dtype=int)
    for row in image:
        for left, right in zip(row[:-1], row[1:]):
            glcm[left, right] += 1
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.05))
    axes[0].imshow(image, cmap="YlGn", vmin=0, vmax=2)
    axes[0].set_title("Cuatro por cuatro, tres grises", fontsize=10, color=GREEN)
    for (i, j), value in np.ndenumerate(image):
        axes[0].text(j, i, str(value), ha="center", va="center", fontsize=10, color=INK)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[1].imshow(glcm, cmap="Greens", vmin=0, vmax=glcm.max())
    axes[1].set_title("Vecino de la derecha (d = 1)", fontsize=10, color=GREEN)
    labels = ["gris 0", "gris 1", "gris 2"]
    axes[1].set_xticks([0, 1, 2], labels, fontsize=8)
    axes[1].set_yticks([0, 1, 2], labels, fontsize=8)
    axes[1].set_xlabel("gris del píxel de la derecha")
    axes[1].set_ylabel("gris del píxel")
    for (i, j), value in np.ndenumerate(glcm):
        axes[1].text(j, i, str(int(value)), ha="center", va="center", fontsize=12, fontweight="bold", color=INK)
    axes[1].tick_params(length=0)
    fig.tight_layout()
    return save_fig(fig, "glcm.png")


def fig_hsv() -> Path:
    fig, ax = plt.subplots(figsize=(7.6, 2.9))
    names = [f"H{i}" for i in range(8)]
    # Ejemplo real de una hoja del smoke del cuaderno HSV (casi todo el matiz en b1 y b2).
    example = [0.001, 0.692, 0.307, 0.0, 0.0, 0.0, 0.0, 0.0]
    colors = ["#C1121F", "#F4A261", "#2D6A4F", "#2A9D8F", "#1D4E89", "#3A0CA3", "#9B2226", "#E63946"]
    ax.bar(names, example, color=colors)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Proporción dentro de la hoja")
    ax.set_title("Matiz de una hoja de ejemplo: casi todo cae en verde", fontsize=11, color=GREEN)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return save_fig(fig, "hsv.png")


def fig_mask() -> Path:
    from matplotlib.patches import Ellipse

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.15))
    scenes = [
        ("#C4B7A6", "A mide toda la foto"),
        ("#F7F4EF", "B y C miden solo la hoja"),
    ]
    for ax, (background, title) in zip(axes, scenes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect("equal")
        ax.add_patch(Rectangle((0.3, 0.3), 9.4, 7.4, facecolor=background, edgecolor="#D6D3D1", lw=0.6))
        ax.add_patch(Ellipse((5.2, 4.0), 5.6, 6.2, facecolor="#2D6A4F", edgecolor="#1B4332", lw=0.8))
        ax.add_patch(Ellipse((6.1, 4.3), 1.5, 1.1, facecolor="#BC6C25", edgecolor="none"))
        ax.set_title(title, fontsize=10, color=GREEN, pad=6)
        ax.axis("off")
    fig.tight_layout()
    return save_fig(fig, "mascara.png")


def fig_split() -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 1.55))
    sizes = [1037, 218, 226]
    labels = ["Train  1.037\naprende", "Val  218\nelige", "Test  226\nmide una vez"]
    colors = [LEAF, GOLD, RUST]
    left = 0
    captions = ["Train · 1.037\naprende", "Val · 218\nelige", "Test · 226\nmide una vez"]
    for size, label, color in zip(sizes, captions, colors):
        ax.barh(0, size, left=left, color=color, height=0.45)
        text_color = INK if color == GOLD else "white"
        ax.text(left + size / 2, 0, label, ha="center", va="center", color=text_color, fontsize=7.5, fontweight="bold")
        left += size
    ax.set_xlim(0, 1481)
    ax.set_yticks([])
    ax.set_xlabel("1.481 hojas con el mismo split en A, B y C")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.tight_layout()
    return save_fig(fig, "split.png")


def draw_cover(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(HexColor(GREEN))
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(HexColor(LEAF))
    canvas.rect(0, 0, 8 * mm, height, fill=1, stroke=0)
    canvas.setFillColor(HexColor(GOLD))
    canvas.rect(0, 0, width, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor(CREAM))
    canvas.setFont("Segoe", 10)
    canvas.drawString(18 * mm, height - 22 * mm, "Proyecto de innovación tecnológica en IA")
    canvas.setFont("Segoe-Light", 28)
    canvas.drawString(18 * mm, height - 48 * mm, "Hojas de café")
    canvas.setFont("Segoe-Bold", 22)
    canvas.drawString(18 * mm, height - 60 * mm, "Qué hicimos, qué decidimos")
    canvas.setFont("Segoe-Bold", 22)
    canvas.drawString(18 * mm, height - 70 * mm, "y cómo se midió cada cosa")
    canvas.setFillColor(HexColor("#D8F3DC"))
    canvas.setFont("Segoe", 11)
    text = canvas.beginText(18 * mm, height - 86 * mm)
    text.setLeading(15)
    text.textLine("Guía corta para estudiar el baseline de RoCoLe")
    text.textLine("y pasarlo a una presentación.")
    text.textLine("Robusta · sana o afectada · semilla 42.")
    canvas.drawText(text)

    canvas.setFillColor(HexColor("#143728"))
    canvas.roundRect(18 * mm, 112 * mm, width - 36 * mm, 40 * mm, 3 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Segoe-Bold", 10)
    canvas.drawString(24 * mm, 140 * mm, "El orden del trabajo")
    canvas.setFont("Segoe", 10)
    steps = canvas.beginText(24 * mm, 132 * mm)
    steps.setLeading(13)
    steps.textLine("1.  Limpiar las fotos y apartarlas por planta, no por foto suelta.")
    steps.textLine("2.  Medir color y textura: primero con el fondo, después solo la hoja, y al final el color HSV.")
    steps.textLine("3.  Comparar mayoría, logística y bosque en las mismas 226 hojas de prueba.")
    canvas.drawText(steps)

    cards = [
        (18 * mm, "0.57", "A  foto completa"),
        (78 * mm, "0.68", "B  solo la hoja"),
        (138 * mm, "0.74", "C  hoja + color HSV"),
    ]
    for x, number, label in cards:
        canvas.setFillColor(HexColor("#143728"))
        canvas.roundRect(x, 48 * mm, 54 * mm, 36 * mm, 3 * mm, fill=1, stroke=0)
        canvas.setFillColor(HexColor(GOLD))
        canvas.setFont("Segoe-Bold", 18)
        canvas.drawString(x + 4 * mm, 68 * mm, number)
        canvas.setFillColor(white)
        canvas.setFont("Segoe", 8)
        canvas.drawString(x + 4 * mm, 58 * mm, label)
        canvas.drawString(x + 4 * mm, 53 * mm, "F1 macro, bosque, test")

    canvas.setFillColor(HexColor(GREEN))
    canvas.setFont("Segoe", 8.5)
    canvas.drawString(18 * mm, 7 * mm, "Lectura de unos 20 minutos.  El número que se cita es el de test, no el de validación.")
    canvas.restoreState()


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(HexColor(GREEN))
    canvas.rect(0, height - 12 * mm, width, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Segoe", 8)
    canvas.drawString(16 * mm, height - 7.5 * mm, "RoCoLe  ·  guía de estudio")
    canvas.drawRightString(width - 16 * mm, height - 7.5 * mm, "Baseline sana / afectada")
    canvas.setFillColor(HexColor(MUTED))
    canvas.setFont("Segoe", 8)
    canvas.drawString(16 * mm, 8 * mm, "Cifras de los cuadernos 04. El test no se reabre para elegir.")
    canvas.drawRightString(width - 16 * mm, 8 * mm, str(doc.page))
    canvas.restoreState()


def img(path: Path, width_mm: float) -> Image:
    image = Image(str(path), width=width_mm * mm, height=width_mm * mm)
    # reportlab Image keeps aspect if we set only width via hAlign after reading size
    from PIL import Image as PILImage

    with PILImage.open(path) as pil:
        ratio = pil.height / pil.width
    image.drawWidth = width_mm * mm
    image.drawHeight = width_mm * mm * ratio
    image.hAlign = "CENTER"
    return image


def build_story(figs: dict) -> list:
    story = [NextPageTemplate("body"), PageBreak()]

    story += section("Cómo leer este documento")
    story.append(
        P(
            "Hay tres experimentos sobre las mismas hojas de café robusta. "
            "La pregunta de todos es la misma: con una foto, ¿esta hoja está sana o afectada? "
            "Lo que cambia es qué píxeles se miden y qué números se le pasan al modelo."
        )
    )
    story.append(img(figs["pipeline"], 174))
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "El resultado en una frase",
            "Medir solo la hoja subió el bosque de 0.57 a 0.68 de F1 macro en test. "
            "Sumar un histograma chico de color lo llevó a 0.74. Sigue sin ser un clasificador de campo: "
            "en el mejor modelo, 35 de 111 hojas enfermas se marcan como sanas.",
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "F1 macro es el promedio del F1 de las dos clases. Cada clase pesa igual. "
            "Por eso se usó para elegir hiperparámetros. El detalle de cómo leer precisión, recall, "
            "macro y weighted está más adelante, con la matriz del experimento C."
        )
    )

    story += section("De dónde salen las hojas")
    story.append(
        P(
            "El conjunto es <b>RoCoLe</b> (Robusta Coffee Leaf, Mendeley): fotos de hojas de café robusta, "
            "sanas o con roya o ácaro, y anotaciones de severidad. BRACOL (arábica) vive aparte y no entra en estos aciertos. "
            "Entrenar en una variedad y probar en la otra sería otro experimento, escrito como tal."
        )
    )
    story.append(P("La etiqueta que aprenden los modelos es binaria.", "h2"))
    story.append(
        bullets(
            [
                "<b>healthy</b>: la hoja se ve sana.",
                "<b>unhealthy</b>: hay roya o ácaro. Esas dos causas se juntan en una sola clase.",
                "La severidad no se usa como medida. Es consecuencia de la etiqueta, no una pista independiente.",
                "La etiqueta fina (ácaro, nivel de roya) queda guardada y no entra en este baseline.",
            ]
        )
    )
    story.append(P("Limpieza antes de medir", "h2"))
    story.append(
        P(
            "Se partió de 1.560 fotos. La tabla de trabajo quedó en <b>1.481</b> hojas, con planta y cara de la hoja. "
            "Lo que se retiró del trabajo (sin borrar los archivos del disco) está documentado en el EDA:"
        )
    )
    story.append(
        bullets(
            [
                "40 duplicados con la misma etiqueta.",
                "15 conflictos de severidad (Astra).",
                "1 par sana / ácaro.",
                "11 pares ácaro / roya, dejados como hold-out.",
            ]
        )
    )
    story.append(
        callout(
            "Por qué importa el duplicado",
            "Si la misma planta cae en train y en test, el modelo puede “reconocer la planta” y el acierto del test queda inflado. "
            "Por eso el reparto no es foto por foto.",
        )
    )

    story += section("El reparto: train, val y test")
    story.append(
        P(
            "Cada planta (y sus duplicados ligados) forma un <b>link_group</b>. "
            "Se repartieron los grupos, no las fotos sueltas: 70 % train, 15 % val, 15 % test, "
            "estratificado y con semilla <b>42</b>. Ese reparto quedó escrito en "
            "<font face='Segoe'>data/featured/rocole/index.csv</font> y los tres experimentos lo reutilizan. No se rehace."
        )
    )
    story.append(img(figs["split"], 174))
    story.append(Spacer(1, 2 * mm))
    story.append(
        styled_table(
            ["Montón", "Hojas", "Para qué sirve", "Qué está prohibido"],
            [
                ["Train", "1.037", "Ajustar el modelo y el escalador", "Elegir mirando el test"],
                ["Val", "218", "Elegir C, árboles, profundidad", "Reajustar con las hojas de test"],
                ["Test", "226", "Medir una sola vez", "Elegir umbral, columnas o modelo"],
            ],
            [28 * mm, 22 * mm, 62 * mm, 62 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "El test tiene 115 sanas y 111 enfermas. Está casi balanceado, así que el accuracy de 0.74 del bosque C "
            "sí se puede leer: no está inflado por una clase enorme. Un modelo que siempre dijera “sana” acertaría cerca de la mitad.",
            "small",
        )
    )

    story += section("Qué se extrae de cada foto")
    story.append(
        P(
            "El modelo no ve la foto. Ve un puñado de números por hoja. "
            "Esos números se calculan igual para todas las fotos, con reglas fijas, antes de entrenar. "
            "El inventario completo trae 9 medidas de color y textura. Los modelos usan 7: se dejó VARI fuera."
        )
    )
    story.append(
        styled_table(
            ["Medida", "Qué resume", "En el modelo"],
            [
                ["exg_mean, exg_std", "Cuánto verde sobra, y qué tan pareja es esa señal", "Sí"],
                ["ngrdi_mean, ngrdi_std", "Verde contra rojo", "Sí"],
                ["vari_mean, vari_std", "Verde contra rojo, restando azul", "No. Se dispara"],
                ["glcm_contrast", "Cambios bruscos de gris entre vecinos", "Sí"],
                ["glcm_homogeneity", "Vecinos parecidos, zonas suaves", "Sí"],
                ["glcm_energy", "Textura dominada por pocos pares de gris", "Sí"],
            ],
            [42 * mm, 88 * mm, 44 * mm],
        )
    )

    story.append(P("Color: tres índices sobre RGB", "h2"))
    story.append(
        P(
            "Cada píxel tiene rojo R, verde G y azul B. Primero se pasa cada canal a proporción de la suma, "
            "para que la luz fuerte no cambie el índice solo por estar más clara: "
            "r = R / (R+G+B), y lo mismo para g y b. Un epsilon pequeño evita dividir por cero."
        )
    )
    story.append(P("ExG = 2g − r − b", "formula"))
    story.append(
        P(
            "<b>Exceso de verde.</b> Una hoja sana empuja este número hacia arriba porque el verde gana al rojo y al azul. "
            "Se guardan la media y la desviación: la media dice el tono general; la desviación dice si la hoja es pareja o tiene manchas."
        )
    )
    story.append(P("NGRDI = (G − R) / (G + R)", "formula"))
    story.append(
        P(
            "<b>Verde contra rojo.</b> Sube donde el verde le gana al rojo y baja donde aparece pardo, amarillo o roya. "
            "También se resume con media y desviación."
        )
    )
    story.append(P("VARI = (G − R) / (G + R − B)", "formula"))
    story.append(
        P(
            "<b>Se calculó y se dejó fuera.</b> El denominador se acerca a cero en píxeles donde el azul casi cancela verde más rojo. "
            "En train, la mediana de vari_mean es 0.14, un número razonable, pero el mínimo llega a cientos de miles negativos "
            "y el máximo a más de un millón. Esas colas aplastan cualquier gráfico y dominarían a la logística. "
            "El CSV conserva las columnas. Los baselines no las usan. Decisión: <b>drop_vari</b>."
        )
    )

    story.append(P("Textura: GLCM en una frase", "h2"))
    story.append(
        P(
            "La matriz de coocurrencia de grises cuenta una sola cosa: con qué frecuencia un tono de gris tiene al lado otro tono. "
            "No usa el color. La foto se pasa a gris y se cuantiza a <b>32 niveles</b> (con 256 la matriz sería de 256×256 y casi vacía). "
            "Se miran vecinos a <b>distancia 1</b> y <b>ángulo 0</b> (el píxel de la derecha). Una sola dirección, a propósito, para que el número sea comparable."
        )
    )
    story.append(img(figs["glcm"], 150))
    story.append(
        P(
            "El dibujo es un ejemplo chico, no una hoja real. A la izquierda, unos grises. A la derecha, cuántas veces un gris tiene a otro a su lado. "
            "De esa matriz salen tres resúmenes:",
            "small",
        )
    )
    story.append(
        bullets(
            [
                "<b>Contraste.</b> Sube cuando los vecinos son muy distintos: bordes, nervaduras marcadas, manchas abruptas.",
                "<b>Homogeneidad.</b> Sube cuando los vecinos se parecen: zonas lisas.",
                "<b>Energía.</b> Sube cuando pocos pares de gris se repiten mucho: la textura está “ordenada” o es muy uniforme.",
            ]
        )
    )

    story.append(P("La máscara: dejar el fondo afuera", "h2"))
    story.append(img(figs["mask"], 150))
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "En el experimento A esos índices y el GLCM se calculan sobre la foto entera: hoja, mesa, mano, sombra. "
            "El fondo puede parecer “textura” o cambiar el verde medio. En B y C se usa la máscara oficial de RoCoLe, "
            "las anotaciones <b>COCO de la categoría Leaf</b>. Si una foto tiene varias anotaciones de hoja, se unen (OR)."
        )
    )
    story.append(
        bullets(
            [
                "Color: media y desviación solo de los píxeles que la máscara marca como hoja.",
                "Textura: se recorta al rectángulo de la máscara y lo que no es hoja, dentro de ese rectángulo, se pone en gris 0. Así el fondo lejano no entra.",
                "Si no hay máscara, la fila queda con error y las medidas en vacío. No se vuelve a la foto completa.",
                "Poner el fuera-de-hoja en 0 puede empujar un poco el contraste en el borde. Es un costo conocido del recorte.",
            ]
        )
    )

    story.append(P("HSV: un histograma chico del color de la hoja", "h2"))
    story.append(
        P(
            "RGB dice cuánto hay de cada luz. HSV reordena el mismo píxel en tres preguntas: "
            "<b>matiz</b> (qué color: rojo, amarillo, verde), <b>saturación</b> (qué tan vivo o qué tan gris) y "
            "<b>valor</b> (qué tan claro). La conversión es la de scikit-image: el matiz queda entre 0 y 1, no en grados. "
            "0 y 1 son el mismo rojo; cerca de 0.33 está el verde."
        )
    )
    story.append(
        P(
            "Sobre los píxeles de la máscara se arma un histograma y se divide por el total, así cada canal suma 1. "
            "Da igual si la hoja ocupa media foto o casi toda: lo que queda es la <b>proporción</b> de color. "
            "El tamaño se eligió chico a propósito: <b>8 cajones de matiz, 4 de saturación y 4 de valor</b>. Son 16 columnas "
            "(hsv_h_b0…b7, hsv_s_b0…b3, hsv_v_b0…b3)."
        )
    )
    story.append(img(figs["hsv"], 160))
    story.append(
        P(
            "En una hoja del inventario, casi el 70 % del matiz cae en el segundo cajón y el 30 % en el tercero: verde. "
            "Una mancha de roya mueve píxeles hacia el amarillo o hacia colores menos saturados, y eso cambia la altura de algunos cajones. "
            "En train, el cajón con más relación con la etiqueta fue hsv_h_b0, cerca de 0.26. Hay señal, y también mucho solape. "
            "Por eso no se armó un modelo solo con HSV: se <b>sumó</b> a las 7 medidas de la máscara.",
            "small",
        )
    )

    story += section("Los tres modelos, siempre en el mismo orden")
    story.append(
        P(
            "Cada experimento entrena los mismos tres modelos. Nada se elige mirando el test. "
            "La logística ve las medidas escaladas; el bosque ve los números crudos, porque los cortes de un árbol no dependen de la escala."
        )
    )
    story.append(
        bullets(
            [
                "<b>Mayoría.</b> Siempre predice la clase más frecuente de train. Es el piso de “no saber nada”. En val su F1 macro es 0.34, porque le pone 0 a la clase que nunca dice.",
                "<b>Logística.</b> Una recta en el espacio de las medidas. Se prueba C en 0.01, 0.1, 1, 10 y 100. En los tres experimentos ganó <b>C = 0.1</b>. El escalador se ajusta solo con train y después solo transforma val y test.",
                "<b>Bosque (Random Forest).</b> Muchos árboles; cada uno vota. Rejilla corta: 100 o 200 árboles, profundidad sin tope, 5 o 10. Peso de clase balanceado y semilla 42. No usa el escalador.",
            ]
        )
    )
    story.append(
        styled_table(
            ["", "A foto", "B máscara", "C máscara + HSV"],
            [
                ["Medidas", "7", "7", "23 (7 + 16)"],
                ["C de la logística", "0.1", "0.1", "0.1"],
                ["Árboles / profundidad", "100 / 10", "200 / 10", "100 / sin tope"],
                ["F1 macro val, bosque", "0.65", "0.74", "0.83"],
                ["F1 macro test, bosque", "0.57", "0.68", "0.74"],
            ],
            [46 * mm, 42 * mm, 42 * mm, 44 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        callout(
            "Val elige. Test informa.",
            "El 0.83 de validación del bosque C no es el número para la presentación. "
            "Val ya se usó para quedarse con 100 árboles sin tope de profundidad. El número honesto, sobre hojas que no eligieron nada, es 0.74.",
            border=AMBER,
            bg="#F8EDE3",
        )
    )

    story += section("Cómo leer la matriz y las dos filas de abajo")
    story.append(
        P(
            "La matriz del bosque C, la que ya miramos, se lee así. Las filas son la verdad. Las columnas son lo que dijo el modelo."
        )
    )
    story.append(
        styled_table(
            ["", "Predicho sana", "Predicho enferma", "Total"],
            [
                ["Real sana", "92", "23  fumigadas de más", "115"],
                ["Real enferma", "35  se escapan", "76  detectadas", "111"],
            ],
            [36 * mm, 40 * mm, 58 * mm, 40 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(img(figs["errors"], 150))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullets(
            [
                "<b>Precisión de enferma = 76 / (76 + 23) = 0.77.</b> De las que el modelo manda a fumigar, el 77 % sí estaban enfermas.",
                "<b>Recall de enferma = 76 / (76 + 35) = 0.68.</b> De las enfermas reales, detecta el 68 %. Las otras 35 pasan como sanas.",
                "<b>Precisión de sana = 92 / (92 + 35) = 0.72.</b> El 0.72 que se ve en el reporte es esta fila, no un promedio.",
                "<b>Recall de sana = 92 / 115 = 0.80.</b>",
                "<b>Accuracy = (92 + 76) / 226 = 0.74.</b>",
            ]
        )
    )
    story.append(P("Macro y weighted", "h2"))
    story.append(
        P(
            "<b>Macro</b> promedia las dos clases con el mismo peso: precisión (0.72 + 0.77) / 2 = 0.75; "
            "recall (0.80 + 0.68) / 2 = 0.74; F1 (0.76 + 0.72) / 2 = 0.74. "
            "<b>Weighted</b> hace el mismo promedio pesado por cuántas hojas tiene cada clase (115 y 111). "
            "Como están casi empatadas, macro y weighted salen iguales. Si una clase fuera rara, el weighted se iría hacia la clase grande "
            "y escondería un recall malo de la chica. Por eso la elección del proyecto es F1 macro."
        )
    )
    story.append(
        P(
            "El recall weighted de este reporte coincide con el accuracy. No son dos evidencias: es la misma cuenta.",
            "small",
        )
    )

    story += section("Los tres experimentos, uno al lado del otro")
    story.append(
        P(
            "Misma pregunta, mismas 226 hojas de test, mismo protocolo. "
            "La gráfica es el bosque, que es el que mejor quedó en val en los tres casos."
        )
    )
    story.append(img(figs["f1"], 165))
    story.append(Spacer(1, 2 * mm))
    story.append(img(figs["confusions"], 174))
    story.append(
        P(
            "Matrices del bosque en test. La celda de abajo a la izquierda son enfermas llamadas sanas. Esa celda baja poco de B a C (36 → 35). "
            "Lo que sí baja es la de arriba a la derecha: sanas llamadas enfermas, de 52 en A a 23 en C.",
            "small",
        )
    )
    story.append(Spacer(1, 2 * mm))

    rows = []
    for proto, model, cm, f1_notebook in (
        (PROTOCOLS[0], "Logística", PROTOCOLS[0]["log_cm"], PROTOCOLS[0]["log_f1_test"]),
        (PROTOCOLS[0], "Bosque", PROTOCOLS[0]["rf_cm"], PROTOCOLS[0]["rf_f1_test"]),
        (PROTOCOLS[1], "Logística", PROTOCOLS[1]["log_cm"], PROTOCOLS[1]["log_f1_test"]),
        (PROTOCOLS[1], "Bosque", PROTOCOLS[1]["rf_cm"], PROTOCOLS[1]["rf_f1_test"]),
        (PROTOCOLS[2], "Logística", PROTOCOLS[2]["log_cm"], PROTOCOLS[2]["log_f1_test"]),
        (PROTOCOLS[2], "Bosque", PROTOCOLS[2]["rf_cm"], PROTOCOLS[2]["rf_f1_test"]),
    ):
        st = cm_stats(cm)
        rows.append(
            [
                f"{proto['key']} {model}",
                f"{st['accuracy']:.2f}",
                f"{st['recall_u']:.2f}",
                f"{st['missed_sick']}",
                f"{st['extra_spray']}",
                f"{f1_notebook:.2f}",
                f"{st['kappa']:.2f}",
            ]
        )
    story.append(
        styled_table(
            ["Test", "Accuracy", "Recall enferma", "Se escapan", "De más", "F1 macro", "Kappa"],
            rows,
            [32 * mm, 22 * mm, 28 * mm, 24 * mm, 20 * mm, 24 * mm, 24 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "Kappa mide el acuerdo por encima de lo que saldría por azar con estas cantidades de sanas y enfermas. "
            "0 es “como adivinar con las proporciones”; 1 sería acuerdo perfecto. El bosque C queda cerca de 0.49. "
            "El F1 macro de la tabla es el que imprimió el cuaderno.",
            "small",
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(P("Qué cambió en cada salto", "h2"))
    story.append(
        bullets(
            [
                "<b>A, foto completa.</b> Logística y bosque quedan casi juntos (0.56 y 0.57). El bosque se equivoca parejo: 52 sanas llamadas enfermas y 45 enfermas llamadas sanas. El fondo está mezclado en las medidas.",
                "<b>B, máscara.</b> Mismas 7 medidas, solo píxeles Leaf. El bosque sube a 0.68. Las enfermas que se escapan bajan de 45 a 36 y las fumigaciones de más de 52 a 37. La comparación A contra B se hizo leyendo lo ya guardado, sin reentrenar.",
                "<b>C, máscara + HSV.</b> Se agregan 16 proporciones de color. El bosque sube a 0.74 y la logística a 0.68. Las sanas mal llamadas bajan a 23. Las enfermas que se escapan se quedan en 35: el color ayudó más a no fumigar sanas que a encontrar las enfermas que faltaban.",
            ]
        )
    )

    story += section("Decisiones que ya quedaron tomadas")
    story.append(
        styled_table(
            ["Decisión", "Por qué"],
            [
                ["Etiqueta binaria", "Primero sana contra afectada. La causa fina queda para después."],
                ["Sin severidad como medida", "La severidad sale de la etiqueta. Usarla sería hacer trampa."],
                ["Sin mezclar BRACOL", "Otra especie, otra captura, otras etiquetas."],
                ["Split por planta, semilla 42", "La misma hoja no puede aprender y examinar."],
                ["F1 macro para elegir", "Las dos clases cuentan igual, aunque una sea un poco más chica."],
                ["Tirar VARI", "El denominador explota. Mediana sana, colas de millones."],
                ["Máscara oficial, sin respaldo", "Si falta la hoja anotada, no se mide la foto entera a escondidas."],
                ["GLCM 32 niveles, d=1, ángulo 0", "Una receta fija y comparable. No se probaron más ángulos."],
                ["HSV 8 / 4 / 4, sumado", "Había señal y mucho solape. No se abrió un modelo solo-HSV."],
                ["class_weight balanced", "El entrenamiento no ignora la clase con menos hojas."],
                ["Escalador solo en logística", "Se ajusta en train. El bosque no lo necesita."],
                ["Hiperparámetros solo en val", "C, árboles y profundidad. Test se mira una vez."],
                ["Pausa de familias nuevas", "Antes de LBP u otra textura: ver si en val sobran bins."],
            ],
            [52 * mm, 122 * mm],
        )
    )

    story += section("El umbral, y qué error duele más")
    story.append(
        P(
            "Hoy el bosque usa el corte de 0.5: si más de la mitad de los árboles votan “enferma”, la hoja se marca enferma. "
            "Eso es lo que hace <font face='Segoe'>predict</font>. El bosque también puede devolver la fracción de votos "
            "(<font face='Segoe'>predict_proba</font>) y el corte se puede mover."
        )
    )
    story.append(
        P(
            "Para este uso, <b>dejar pasar la enfermedad es el error más caro</b>. "
            "Una enferma llamada sana no se trata, la roya sigue y puede pasar a las vecinas. "
            "Una sana llamada enferma cuesta un químico de más: es plata y es un costo real, y se puede acotar. "
            "La planta perdida no. Con el corte de 0.5 el modelo ya está del lado que duele más: 35 escapan y 23 se fumigan de más."
        )
    )
    story.append(
        callout(
            "Dónde se haría, y dónde no",
            "El corte se elegiría en val, después de tener el bosque final ajustado en train, y antes de tocar el test. "
            "Se prueban cortes (0.5, 0.4, 0.3…) y se mira cuántas enfermas se recuperan contra cuántas sanas se fumigan de más. "
            "Ese número queda fijo y el test se mide una vez con él. "
            "Este test de 226 hojas ya se abrió. Elegir el corte mirando estos 35 dejaría el próximo número sucio. "
            "Todavía no está en el cuaderno.",
            border=AMBER,
            bg="#F8EDE3",
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "Bajar el corte de “enferma” mueve hojas de una celda a la otra. Algunas de las 35 entran a detectadas, "
            "y algunas de las 92 sanas bien clasificadas pasan a fumigadas de más. No hay forma de bajar una sin subir la otra. "
            "La fracción de votos no es una probabilidad calibrada: 0.3 quiere decir “el 30 % de los árboles votó enferma”.",
        )
    )

    story += section("Qué se puede decir en la presentación")
    story.append(
        P(
            "Diez diapositivas alcanzan. En cada una, una idea. El número que se dice en voz alta es el de test."
        )
    )
    slides = [
        ("1. El problema", "Una foto de una hoja no siempre se lee igual: luz, ángulo, fondo. El apoyo es preliminar, no un veredicto de campo."),
        ("2. El dato", "RoCoLe, robusta, 1.481 hojas tras limpieza. Etiqueta: sana o afectada. Árabica no se mezcla."),
        ("3. El reparto", "Por planta, semilla 42. 1.037 aprenden, 218 eligen, 226 examinan una vez. Mostrar la barra de split."),
        ("4. Qué ve el modelo", "No ve la foto. Ve verde de más, verde contra rojo, y tres números de textura. VARI se calculó y se tiró."),
        ("5. La máscara", "A mide hoja y fondo. B mide solo la hoja anotada en COCO. Mostrar el esquema de las dos fotos."),
        ("6. El color HSV", "16 proporciones dentro de la hoja: 8 de matiz, 4 de saturación, 4 de brillo. Se suman; no reemplazan."),
        ("7. El protocolo", "Mayoría, logística y bosque. Val elige. Test informa. F1 macro, peso de clase balanceado."),
        ("8. El salto", "Bosque en test: 0.57 → 0.68 → 0.74. Mostrar las tres barras. Decir que val está más alto y no se cita."),
        ("9. El error que importa", "Matriz C: 35 enfermas se escapan, 23 sanas se fumigarían de más. Dejar pasar la roya duele más."),
        ("10. El límite", "No está listo para campo. Siguiente paso, si se hace: umbral en val, sin reabrir este test. Pausa de familias nuevas."),
    ]
    slide_rows = []
    for title, body in slides:
        slide_rows.append([P(title, "slide_title"), P(body, "slide_body")])
    slide_table = Table(slide_rows, colWidths=[42 * mm, 132 * mm])
    slide_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), HexColor(SAGE)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, HexColor(LINE)),
            ]
        )
    )
    story.append(slide_table)
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "Frase para cerrar",
            "Quitar el fondo mejoró el diagnóstico más que cambiar de modelo. "
            "El color de la hoja, contado en pocos cajones, mejoró otra vez. "
            "El hueco que queda es el mismo: una de cada tres hojas enfermas todavía pasa como sana.",
        )
    )

    story += section("Dónde está cada cosa")
    story.append(
        styled_table(
            ["Pieza", "Dónde"],
            [
                ["Limpieza y split", "notebooks/rocole/01-eda-rocole.ipynb"],
                ["Medidas sin máscara", "notebooks/rocole/A-full/02 y 03"],
                ["Baseline foto completa", "notebooks/rocole/A-full/04"],
                ["Medidas con máscara", "notebooks/rocole/B-masked/02 y 03"],
                ["Baseline máscara y comparación", "B-masked/04 y 05"],
                ["Histograma HSV y su EDA", "notebooks/rocole/C-hsv-masked/02 y 03"],
                ["Baseline 7 + 16", "notebooks/rocole/C-hsv-masked/04"],
                ["Tablas y figuras", "experiments/results/rocole/"],
                ["Índice del split", "data/featured/rocole/index.csv"],
            ],
            [58 * mm, 116 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Esta guía resume los cuadernos ya corridos. No reentrena, no mueve el umbral y no reabre el test. "
            "Si un número de aquí y uno de un CSV viejo no coinciden, manda la matriz impresa en el cuaderno 04 de ese experimento.",
            "small",
        )
    )
    return story


def main() -> None:
    global S
    setup_fonts()
    S = styles()
    figs = {
        "pipeline": fig_pipeline(),
        "f1": fig_f1(),
        "confusions": fig_confusions(),
        "errors": fig_errors(),
        "glcm": fig_glcm(),
        "hsv": fig_hsv(),
        "mask": fig_mask(),
        "split": fig_split(),
    }
    doc = BaseDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        title="RoCoLe: decisiones, extracción y resultados del baseline",
        author="Diagnóstico de hojas de café",
    )
    frame_cover = Frame(0, 0, A4[0], A4[1], id="cover", showBoundary=0)
    frame_body = Frame(16 * mm, 16 * mm, A4[0] - 32 * mm, A4[1] - 32 * mm, id="body", showBoundary=0)
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[frame_cover], onPage=draw_cover),
            PageTemplate(id="body", frames=[frame_body], onPage=draw_page),
        ]
    )
    doc.build(build_story(figs))
    print(OUT_PDF)


if __name__ == "__main__":
    main()
