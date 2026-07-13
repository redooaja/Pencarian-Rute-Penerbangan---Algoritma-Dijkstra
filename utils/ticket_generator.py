

import random
import string
import datetime

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


# ==========================================
# WARNA TEMA (selaras dengan tema "Skyline" di app)
# ==========================================
NAVY = HexColor("#0F172A")
BLUE = HexColor("#2563EB")
CYAN = HexColor("#06B6D4")
WHITE = HexColor("#FFFFFF")
LIGHT_BG = HexColor("#F1F5F9")
MUTED = HexColor("#64748B")
BORDER = HexColor("#E2E8F0")


def _generate_kode_booking():
    """Membuat kode booking acak 6 karakter, mirip PNR maskapai sungguhan."""
    huruf = "".join(random.choices(string.ascii_uppercase, k=3))
    angka = "".join(random.choices(string.digits, k=3))
    return huruf + angka


def _generate_seat():
    baris = random.randint(1, 32)
    kolom = random.choice("ABCDEF")
    return f"{baris}{kolom}"


def _generate_gate():
    return f"{random.choice('ABCD')}{random.randint(1, 24)}"


def _draw_barcode(c, x, y, width, height):
    """Barcode dekoratif (bukan barcode scannable sungguhan)."""
    bar_x = x
    while bar_x < x + width:
        bar_w = random.choice([0.6, 1.2, 1.8, 2.4]) * mm
        c.setFillColor(NAVY)
        c.rect(bar_x, y, bar_w, height, stroke=0, fill=1)
        bar_x += bar_w + random.choice([0.8, 1.4]) * mm


def generate_ticket(
    nama_penumpang,
    kode_asal,
    nama_asal,
    kota_asal,
    kode_tujuan,
    nama_tujuan,
    kota_tujuan,
    path,
    cost,
    total_distance,
    output_path="tiket_elektronik.pdf",
):
    """
    Membuat PDF tiket elektronik bergaya boarding pass.

    Parameters
    ----------
    nama_penumpang : str
    kode_asal, nama_asal, kota_asal : str        -> info bandara asal
    kode_tujuan, nama_tujuan, kota_tujuan : str   -> info bandara tujuan
    path : list[str]                              -> urutan kode bandara (rute)
    cost : int/float                               -> total biaya
    total_distance : int/float                     -> total jarak (KM)
    output_path : str                              -> path file pdf hasil

    Returns
    -------
    str : path file PDF yang dihasilkan
    """

    kode_booking = _generate_kode_booking()
    seat = _generate_seat()
    gate = _generate_gate()
    waktu_cetak = datetime.datetime.now()

    tanggal_cetak = waktu_cetak.strftime("%d-%m-%Y")
    jam_cetak = waktu_cetak.strftime("%H:%M:%S")
    jumlah_transit = max(0, len(path) - 2)

    waktu_cetak = datetime.datetime.now()

    tanggal_cetak = waktu_cetak.strftime("%d-%m-%Y")
    jam_cetak = waktu_cetak.strftime("%H:%M:%S")

    # Ukuran boarding pass: 260mm x 100mm (landscape, mirip tiket sungguhan)
    PAGE_W, PAGE_H = 260 * mm, 100 * mm
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))

    # ===== BACKGROUND UTAMA =====
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # ===== STUB UTAMA (kiri, ~72% lebar) =====
    main_w = PAGE_W * 0.72

    # Header gradient-ish band (navy -> blue simulasi dgn 2 blok)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 18 * mm, main_w, 18 * mm, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.rect(0, PAGE_H - 18 * mm, main_w * 0.35, 18 * mm, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(8 * mm, PAGE_H - 12 * mm, "✈ PENCARI RUTE PENERBANGAN")
    c.setFont("Helvetica", 8)
    c.drawString(8 * mm, PAGE_H - 16.5 * mm, "E-TICKET / BOARDING PASS")

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(main_w - 8 * mm, PAGE_H - 12 * mm, f"Kode Booking")
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(main_w - 8 * mm, PAGE_H - 17 * mm, kode_booking)

    # ===== RUTE BESAR (kode bandara ala boarding pass) =====
    route_y = PAGE_H - 40 * mm

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(8 * mm, route_y, kode_asal)

    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(8 * mm, route_y - 5 * mm, f"{nama_asal}")
    c.drawString(8 * mm, route_y - 9 * mm, f"{kota_asal}")

    # Garis + ikon pesawat di tengah
    mid_x = main_w / 2
    c.setStrokeColor(BORDER)
    c.setLineWidth(1.2)
    c.line(45 * mm, route_y + 8 * mm, main_w - 45 * mm, route_y + 8 * mm)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(mid_x, route_y + 10 * mm, "✈")
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    label_transit = "Langsung" if jumlah_transit == 0 else f"{jumlah_transit} Transit"
    jalur_dijkstra = " ➜ ".join(path)

    c.setFillColor(NAVY)
    c.setFont("Helvetica", 8)

    c.drawString(
        8 * mm,
        16 * mm,
        f"Jalur Optimal Dijkstra : {jalur_dijkstra}"
    )
    c.drawCentredString(mid_x, route_y + 4.5 * mm, label_transit)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 30)
    c.drawRightString(main_w - 8 * mm, route_y, kode_tujuan)

    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(main_w - 8 * mm, route_y - 5 * mm, f"{nama_tujuan}")
    c.drawRightString(main_w - 8 * mm, route_y - 9 * mm, f"{kota_tujuan}")

    # ===== INFO GRID (penumpang, tanggal, gate, kursi, boarding) =====
    grid_y = 22 * mm
    labels = [
    "PENUMPANG",
    "TANGGAL CETAK",
    "JAM CETAK",
    "GATE",
    "KURSI"
    ]

    values = [
        nama_penumpang.upper(),
        tanggal_cetak,
        jam_cetak,
        gate,
        seat
    ]
    col_w = main_w / len(labels)

    for i, (lab, val) in enumerate(zip(labels, values)):
        x = 8 * mm + i * col_w
        c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)

    c.drawString(
    8 * mm,
    12 * mm,
    f"Total Biaya : Rp {cost:,}"
    )
    
    c.drawString(
        70 * mm,
        12 * mm,
        f"Jarak : {total_distance:,} KM"
    )
    
    c.drawString(
        120 * mm,
        12 * mm,
        f"Transit : {jumlah_transit}"
    )
    
    c.drawString(
        150 * mm,
        12 * mm,
        "Algoritma : Dijkstra"
    )




    # Barcode dekoratif
    _draw_barcode(c, 8 * mm, 2 * mm, main_w - 16 * mm, 4 * mm)

    # ===== GARIS PUTUS-PUTUS PEMISAH (perforasi) =====
    c.setDash(2, 2)
    c.setStrokeColor(BORDER)
    c.setLineWidth(1)
    c.line(main_w, 0, main_w, PAGE_H)
    c.setDash([], 0)

    # Lubang "sobekan" tiket
    c.setFillColor(WHITE)
    c.circle(main_w, PAGE_H, 4 * mm, stroke=0, fill=1)
    c.circle(main_w, 0, 4 * mm, stroke=0, fill=1)

    # ===== STUB KANAN (kupon kecil) =====
    stub_x = main_w
    stub_w = PAGE_W - main_w

    c.setFillColor(NAVY)
    c.rect(stub_x, 0, stub_w, PAGE_H, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(stub_x + stub_w / 2, PAGE_H - 12 * mm, "BOARDING PASS")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(stub_x + stub_w / 2, PAGE_H - 25 * mm, kode_asal)
    c.setFont("Helvetica", 9)
    c.drawCentredString(stub_x + stub_w / 2, PAGE_H - 30 * mm, "ke")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(stub_x + stub_w / 2, PAGE_H - 38 * mm, kode_tujuan)

    info_stub = [
    ("PENUMPANG", nama_penumpang.upper()[:14]),
    ("KODE BOOKING", kode_booking),
    ("TANGGAL", tanggal_cetak),
    ("JAM", jam_cetak),
    ("KURSI", seat),
    ]

    y_cursor = PAGE_H - 48 * mm
    for lab, val in info_stub:
        c.setFillColor(CYAN)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(stub_x + stub_w / 2, y_cursor, lab)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(stub_x + stub_w / 2, y_cursor - 4.5 * mm, val)
        y_cursor -= 10 * mm

    c.save()
    return output_path