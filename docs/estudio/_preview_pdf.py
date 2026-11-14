import os
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(r"docs/estudio-rocole-baselines.pdf")
print("pages", len(pdf))
out = r"docs/estudio/_preview"
os.makedirs(out, exist_ok=True)
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.3)
    img = bitmap.to_pil()
    img.save(os.path.join(out, f"page-{i+1:02d}.png"))
    print(i + 1, img.size)
