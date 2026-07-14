import random
import string
import datetime
import uuid
import os

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


def _generate_gate(seed_text=None):
    """
    Simulasi gate keberangkatan Bandara Supadio Pontianak (PNK).
    Terminal baru Bandara Supadio memiliki 7 (tujuh) unit garbarata
    yang beroperasi sejak tahun 2020, sehingga gate disimulasikan
    dari A1 sampai A7.

    Jika seed_text diberikan, pemilihan gate bersifat deterministik
    (kode booking/rute yang sama akan selalu mendapat gate yang sama).
    """

    gate_supadio = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
    ]

    if seed_text:
        rnd = random.Random(seed_text)
        return rnd.choice(gate_supadio)

    return random.choice(gate_supadio)


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
    output_path=None,
):

    kode_booking = _generate_kode_booking()
    seat = _generate_seat()
    gate = _generate_gate(seed_text=kode_booking + kode_asal + kode_tujuan)

    waktu_cetak = datetime.datetime.now()
    tanggal_cetak = waktu_cetak.strftime("%d-%m-%Y")
    jam_cetak = waktu_cetak.strftime("%H:%M:%S")
    jumlah_transit = max(0, len(path) - 2)

    # Nama file unik per tiket, disimpan di folder sementara agar tidak
    # saling menimpa antar penumpang/rute yang berbeda.
    if output_path is None:
        os.makedirs("output_tiket", exist_ok=True)
        output_path = os.path.join(
            "output_tiket",
            f"tiket_{kode_asal}_{kode_tujuan}_{uuid.uuid4().hex[:6]}.pdf",
        )

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
    c.drawString(8 * mm, PAGE_H - 12 * mm, "\u2708 PENCARI RUTE PENERBANGAN")
    c.setFont("Helvetica", 8)
    c.drawString(8 * mm, PAGE_H - 16.5 * mm, "E-TICKET / BOARDING PASS")

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(main_w - 8 * mm, PAGE_H - 12 * mm, "Kode Booking")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(CYAN)
    c.drawRightString(main_w - 8 * mm, PAGE_H - 17 * mm, kode_booking)

    # ===== RUTE BESAR (kode bandara ala boarding pass) =====
    route_y = PAGE_H - 40 * mm  # 60mm

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
    c.drawCentredString(mid_x, route_y + 10 * mm, "\u2708")

    jumlah_transit_label = "Langsung" if jumlah_transit == 0 else f"{jumlah_transit} Transit"
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawCentredString(mid_x, route_y + 4.5 * mm, jumlah_transit_label)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 30)
    c.drawRightString(main_w - 8 * mm, route_y, kode_tujuan)

    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(main_w - 8 * mm, route_y - 5 * mm, f"{nama_tujuan}")
    c.drawRightString(main_w - 8 * mm, route_y - 9 * mm, f"{kota_tujuan}")

    # ===== GARIS PEMISAH SEBELUM INFO GRID =====
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.7)
    c.line(8 * mm, 40 * mm, main_w - 8 * mm, 40 * mm)

    # ===== INFO GRID (penumpang, tanggal, jam, gate, kursi) =====
    grid_label_y = 34 * mm
    grid_value_y = 34 * mm - 5.5 * mm

    labels = ["PENUMPANG", "TANGGAL CETAK", "JAM CETAK", "GATE", "KURSI"]
    values = [
        nama_penumpang.upper(),
        tanggal_cetak,
        jam_cetak,
        gate,
        seat,
    ]

    grid_left = 8 * mm
    grid_right = main_w - 8 * mm
    col_w = (grid_right - grid_left) / len(labels)

    for i, (lab, val) in enumerate(zip(labels, values)):
        x = grid_left + i * col_w
        is_gate = lab == "GATE"

        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawString(x, grid_label_y, lab)

        c.setFillColor(CYAN if is_gate else NAVY)
        c.setFont("Helvetica-Bold", 11)
        val_text = str(val)
        # Pangkas otomatis kalau teks kepanjangan untuk kolom PENUMPANG
        if lab == "PENUMPANG" and len(val_text) > 16:
            val_text = val_text[:15] + "…"
        c.drawString(x, grid_value_y, val_text)

    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 6)
    c.drawString(
        grid_left,
        grid_value_y - 6 * mm,
        "Gate keberangkatan disimulasikan berdasarkan garbarata Bandara Supadio (PNK)",
    )

    # ===== BARIS RINGKASAN PERJALANAN (biaya, jarak, transit, algoritma) =====
    info_y = 14 * mm

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(grid_left, info_y, f"Total Biaya: Rp {cost:,}")
    c.drawString(grid_left + 62 * mm, info_y, f"Jarak: {total_distance:,} KM")
    c.drawString(grid_left + 100 * mm, info_y, f"Transit: {jumlah_transit}")
    c.drawString(grid_left + 130 * mm, info_y, "Algoritma: Dijkstra")

    jalur_dijkstra = " \u279c ".join(path)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)
    jalur_text = f"Jalur Optimal: {jalur_dijkstra}"
    if len(jalur_text) > 95:
        jalur_text = jalur_text[:92] + "..."
    c.drawString(grid_left, info_y - 5 * mm, jalur_text)

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
        ("GATE", gate),
        ("TANGGAL", tanggal_cetak),
        ("JAM", jam_cetak),
        ("KURSI", seat),
    ]

    y_cursor = PAGE_H - 48 * mm
    for lab, val in info_stub:
        highlight = lab == "GATE"
        c.setFillColor(CYAN)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(stub_x + stub_w / 2, y_cursor, lab)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13 if highlight else 9)
        c.drawCentredString(stub_x + stub_w / 2, y_cursor - (5.5 if highlight else 4.5) * mm, val)
        y_cursor -= 10 * mm

    c.save()
    return output_path