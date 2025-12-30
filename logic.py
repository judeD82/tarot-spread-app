from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO


def generate_tarot_spread_pdf(
    spread_name: str,
    theme: str,
    positions: list[str]
) -> BytesIO:
    """
    Generates a printable PDF for a custom tarot spread.
    Returns a BytesIO buffer ready for download.
    """

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 2 * cm

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y, spread_name)
    y -= 1.2 * cm

    # Theme
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Theme / Intention")
    y -= 0.6 * cm

    c.setFont("Helvetica", 11)
    text = c.beginText(2 * cm, y)
    for line in theme.split("\n"):
        text.textLine(line)
    c.drawText(text)

    y = text.getY() - 1 * cm

    # Positions
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Card Positions")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    for idx, pos in enumerate(positions, start=1):
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 12)

        c.drawString(2 * cm, y, f"{idx}. {pos}")
        y -= 0.8 * cm

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

