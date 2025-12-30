from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO


def generate_tarot_spread_pdf(spread_name, theme, positions, layout_def):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 2 * cm, spread_name)

    # Theme
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 3.2 * cm, theme)

    # Tarot card size for print (larger than preview)
    card_w = 4 * cm
    card_h = 7 * cm
    gap = 1 * cm

    cols = layout_def["cols"]
    rows = len(layout_def["rows"])

    grid_width = cols * card_w + (cols - 1) * gap
    grid_height = rows * card_h + (rows - 1) * gap

    start_x = (width - grid_width) / 2
    start_y = height - 5 * cm

    for r, row in enumerate(layout_def["rows"]):
        for c_idx, cell in enumerate(row):
            if cell.startswith("c"):
                i = int(cell[1:])
                x = start_x + c_idx * (card_w + gap)
                y = start_y - r * (card_h + gap)

                # Card outline
                c.roundRect(x, y, card_w, card_h, 14, stroke=1, fill=0)

                # Card label
                c.setFont("Helvetica", 10)
                c.drawCentredString(
                    x + card_w / 2,
                    y + card_h / 2,
                    positions[i]
                )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
