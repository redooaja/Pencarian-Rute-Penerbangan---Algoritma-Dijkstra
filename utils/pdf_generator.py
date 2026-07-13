from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    asal,
    tujuan,
    path,
    cost,
    total_distance
):

    pdf_file = "hasil_rute.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "PENCARIAN RUTE PENERBANGAN",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Penerapan Graph dan Algoritma Dijkstra dalam Pencarian Rute Penerbangan dengan Biaya Termurah Antar Bandara di Indonesia",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>INFORMASI PERJALANAN</b>",
            styles["Heading3"]
        )
    )

    content.append(
        Paragraph(
            f"Bandara Asal : {asal}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Bandara Tujuan : {tujuan}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>RUTE OPTIMAL</b>",
            styles["Heading3"]
        )
    )

    content.append(
        Paragraph(
            " ➜ ".join(path),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>RINGKASAN HASIL</b>",
            styles["Heading3"]
        )
    )

    content.append(
        Paragraph(
            f"Total Biaya : Rp {cost:,}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Jumlah Transit : {max(0, len(path)-2)}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Bandara Dilalui : {len(path)}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Jarak Perjalanan : {total_distance:,} KM",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>DETAIL JALUR</b>",
            styles["Heading3"]
        )
    )

    for i, bandara in enumerate(path, start=1):

        content.append(
            Paragraph(
                f"{i}. {bandara}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Algoritma : Dijkstra",
            styles["Italic"]
        )
    )

    content.append(
        Paragraph(
            "Pencarian Rute Penerbangan © 2026",
            styles["Italic"]
        )
    )

    doc.build(content)

    return pdf_file