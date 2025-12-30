from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO


def generate_tarot_spread_pdf(spread_name, theme, positions, layout_def):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 2 * cm, spread_name)

    # Theme
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 3 * cm, theme)

    # Card sizing (tarot proportion)
    card_w = 3 * cm
    card_h = 5 * cm
    gap = 0.8 * cm

    grid_cols = layout_def["cols"]
    grid_rows = len(layout_def["rows"])

    grid_width = grid_cols * card_w + (grid_cols - 1) * gap
    grid_height = grid_rows * card_h + (grid_rows - 1) * gap

    start_x = (width - grid_width) / 2
    start_y = height - 6 * cm

    for row_idx, row in enumerate(layout_def["rows"]):
        for col_idx, cell in enumerate(row):
            if cell.startswith("c"):
                i = int(cell[1:])
                x = start_x + col_idx * (card_w + gap)
                y = start_y - row_idx * (card_h + gap)

                # Card outline
                c.roundRect(x, y, card_w, card_h, 10, stroke=1, fill=0)

                # Card label
                c.setFont("Helvetica", 9)
                c.drawCentredString(
                    x + card_w / 2,
                    y + card_h / 2,
                    positions[i]
                )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
