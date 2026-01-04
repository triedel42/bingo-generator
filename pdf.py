from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit


def generate_bingo_pdf(filename, phrases, identifier):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    if len(phrases) < 24:
        raise ValueError("You need at least 24 phrases for a 5x5 grid.")

    grid_phrases = phrases[:24]
    grid_phrases.insert(12, "FREE")

    # Grid Settings
    grid_size = 16 * cm
    cell_size = grid_size / 5
    margin_left = (width - grid_size) / 2
    margin_bottom = (height - grid_size) / 2

    # Top-Left Identifier
    c.setFont("Helvetica", 10)
    c.drawString(1 * cm, height - 1.5 * cm, identifier)

    # Main Title
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, margin_bottom + grid_size + 1 * cm, "42bingo")

    # Draw Grid and Text
    for i in range(5):  # Rows
        for j in range(5):  # Columns
            x = margin_left + j * cell_size
            y = margin_bottom + (4 - i) * cell_size

            # Draw Cell Border
            c.setLineWidth(1)
            c.rect(x, y, cell_size, cell_size)

            phrase = grid_phrases[i * 5 + j]

            # Font Logic
            if phrase == "FREE":
                c.setFont("Helvetica-Bold", 14)
            else:
                c.setFont("Helvetica", 6)

            # Wrap text to fit inside the cell width (minus some padding)
            wrapped_text = simpleSplit(phrase, c._fontname, c._fontsize, cell_size - 10)

            # Calculate vertical start to center multiple lines
            line_height = c._fontsize * 1.2
            total_text_height = len(wrapped_text) * line_height
            start_y = y + (cell_size / 2) + (total_text_height / 2) - line_height

            for line in wrapped_text:
                c.drawCentredString(x + cell_size / 2, start_y, line)
                start_y -= line_height

    c.showPage()
    c.save()
