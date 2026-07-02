import streamlit as st
import pandas as pd

from streamlit_folium import st_folium
from utils.map_utils import create_map

from utils.route_details import get_route_details
from algorithms.dijkstra import dijkstra
from utils.load_data import load_graph
from utils.distance import calculate_total_distance
from utils.pdf_generator import generate_pdf

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Flight Route Finder",
    page_icon="✈️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS — TEMA "SKYLINE"
# (Tidak mengubah logika, hanya mempercantik tampilan)
# ==========================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
    --sky-navy: #0F172A;
    --sky-blue: #2563EB;
    --sky-blue-light: #60A5FA;
    --sky-cyan: #06B6D4;
    --sky-bg: #F8FAFC;
    --sky-card: #FFFFFF;
    --sky-border: #E2E8F0;
    --sky-text: #1E293B;
    --sky-muted: #64748B;
    --sky-radius: 16px;
    --sky-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--sky-text);
}

.stApp {
    background: linear-gradient(180deg, #EFF6FF 0%, var(--sky-bg) 320px);
}

/* ===== HERO HEADER ===== */
.hero-banner {
    background: linear-gradient(135deg, var(--sky-navy) 0%, var(--sky-blue) 100%);
    border-radius: var(--sky-radius);
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--sky-shadow);
    position: relative;
    overflow: hidden;
}

.hero-banner::after {
    content: "✈";
    position: absolute;
    right: -10px;
    top: -30px;
    font-size: 11rem;
    opacity: 0.08;
    transform: rotate(20deg);
}

.hero-title {
    color: white;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    color: #DBEAFE;
    font-size: 0.98rem;
    font-weight: 500;
    max-width: 720px;
    line-height: 1.5;
    margin: 0;
}

/* ===== PANEL / CARD ===== */
.sky-panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--sky-navy);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid var(--sky-border);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--sky-card);
    border-radius: var(--sky-radius) !important;
    box-shadow: var(--sky-shadow);
    border: 1px solid var(--sky-border) !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(135deg, var(--sky-blue) 0%, var(--sky-cyan) 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    color: white;
}

/* ===== METRIC ===== */
div[data-testid="stMetric"] {
    background: var(--sky-bg);
    border: 1px solid var(--sky-border);
    border-radius: 12px;
    padding: 0.8rem 0.6rem;
    text-align: center;
}

div[data-testid="stMetric"] {
    background: var(--sky-bg);
    border: 1px solid var(--sky-border);
    border-radius: 12px;
    padding: 0.8rem 0.6rem;
    text-align: center;
    overflow: visible !important;
}

div[data-testid="stMetricLabel"] {
    font-weight: 600;
    color: var(--sky-muted);
    white-space: normal !important;
    overflow: visible !important;
}

div[data-testid="stMetricLabel"] p {
    white-space: normal !important;
    overflow-wrap: break-word !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'Fira Code', monospace;
    color: var(--sky-navy);
    font-weight: 700;
    font-size: clamp(0.85rem, 1.4vw, 1.4rem) !important;
    white-space: normal !important;
    overflow: visible !important;
    overflow-wrap: break-word !important;
    text-overflow: unset !important;
    line-height: 1.25;
    width: 100%;
}

div[data-testid="stMetricValue"] div,
div[data-testid="stMetricValue"] p {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    overflow-wrap: break-word !important;
    max-width: 100% !important;
}

/* ===== SELECTBOX ===== */
div[data-baseweb="select"] {
    border-radius: 10px;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--sky-bg);
    padding: 4px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1rem;
}

.stTabs [aria-selected="true"] {
    background: white;
    box-shadow: var(--sky-shadow);
}

/* ===== DIVIDER lebih tipis & elegan ===== */
hr {
    margin: 1.2rem 0;
    border-color: var(--sky-border);
}

/* ===== CAPTION FOOTER ===== */
.sky-footer {
    text-align: center;
    color: var(--sky-muted);
    font-size: 0.82rem;
    padding-top: 1rem;
}

/* ===== DATAFRAME ===== */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--sky-border);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

graph = load_graph()

airports = pd.read_csv("data/airports.csv")

routes = pd.read_csv("data/routes.csv")

jumlah_bandara = len(airports)

jumlah_rute = len(routes)


# Dropdown menampilkan kode + nama + kota
airport_options = {
    f"{row['kode']} - {row['nama']} ({row['kota']})": row['kode']
    for _, row in airports.iterrows()
}

# Dictionary nama bandara
airport_dict = {
    row["kode"]: row["nama"]
    for _, row in airports.iterrows()
}

# Dictionary kota
airport_city = {
    row["kode"]: row["kota"]
    for _, row in airports.iterrows()
}

# Dictionary info lengkap
airport_full_info = {
    row["kode"]: f"{row['kode']} ({row['nama']} - {row['kota']})"
    for _, row in airports.iterrows()
}

# ==========================================
# HEADER (versi hero banner)
# ==========================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✈️ Sistem Pencarian Rute Penerbangan</div>
    <p class="hero-subtitle">
        Penerapan Algoritma Dijkstra dalam Optimasi Rute Penerbangan Berbiaya
        Termurah Antar Bandara di Indonesia Berbasis Web
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LAYOUT
# ==========================================

left_col, right_col = st.columns([1, 2])

# ==========================================
# PANEL KIRI
# ==========================================

with left_col:

    with st.container(border=True):

        st.markdown('<div class="sky-panel-title">🔎 Pencarian Rute</div>', unsafe_allow_html=True)

        asal_display = st.selectbox(
            "Bandara Asal",
            list(airport_options.keys())
        )

        asal = airport_options[asal_display]

        tujuan_display = st.selectbox(
            "Bandara Tujuan",
            list(airport_options.keys()),
            index=1
        )

        tujuan = airport_options[tujuan_display]

        if "cari" not in st.session_state:
            st.session_state.cari = False

        if st.button(
            "🔍 Cari Rute Termurah",
            use_container_width=True
        ):
            st.session_state.cari = True

    st.write("")

    with st.container(border=True):

        st.markdown('<div class="sky-panel-title">📊 Statistik Sistem</div>', unsafe_allow_html=True)

        c1, c2, c3= st.columns(3)

        with c1:
            st.metric(
                "Bandara",
                jumlah_bandara
            )

        with c2:
            st.metric(
                "Rute",
                jumlah_rute
            )

        with c3:
            st.metric(
                "Algoritma",
                "Dijkstra"
            )

        with st.expander(f"📋 Lihat Semua Rute ({jumlah_rute})"):
            st.dataframe(
                routes,
                use_container_width=True,
                height=300
            )


# ==========================================
# PANEL KANAN
# ==========================================

with right_col:

    with st.container(border=True):

        st.markdown('<div class="sky-panel-title">🗺️ Hasil Pencarian</div>', unsafe_allow_html=True)

        if not st.session_state.cari:

            default_map = create_map(
                airports
            )

            st_folium(
                default_map,
                width=None,
                height=650
            )

            st.info(
                "Silakan pilih bandara asal dan tujuan."
            )

        if st.session_state.cari:

            if asal == tujuan:

                st.warning(
                    "Bandara asal dan tujuan tidak boleh sama."
                )

            else:

                try:

                    with st.spinner("🔍 Menghitung rute termurah dengan algoritma Dijkstra..."):

                        path, cost = dijkstra(
                            graph,
                            asal,
                            tujuan
                        )
                        segment_details, total_cost = get_route_details(path)

                        total_distance = calculate_total_distance(
                            path,
                            airports
                        )



                        route_names = [
                            f"{airport_dict[kode]} ({airport_city[kode]})"
                            for kode in path
                        ]

                        route_map = create_map(
                            airports,
                            path
                        )

                    st.success(
                        "Rute berhasil ditemukan."
                    )

                    st_folium(
                    route_map,
                    width=None,
                    height=700
                    )

                    st.info(
                        f"✈️ {airport_full_info[asal]} ➜ {airport_full_info[tujuan]}"
                    )


                    # =====================
                    # METRIC
                    # =====================

                    # =====================
                    # METRIC BARIS 1
                    # =====================

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.metric(
                            "💰 Total Biaya",
                            f"Rp {cost/1_000_000:.2f} Jt"
                        )

                    with m2:
                        st.metric(
                            "🛫 Transit",
                            max(0, len(path)-2)
                        )

                    with m3:
                        st.metric(
                            "🏢 Bandara",
                            len(path)
                        )

                    with m4:
                        st.metric(
                            "📍 Jarak",
                            f"{total_distance:,} KM"
                        )

                    st.subheader("🧠 Hasil Optimasi Rute Dijkstra")

                    st.success(f"""
                    Bandara Asal :
                    {airport_full_info[asal]}

                    Bandara Tujuan :
                    {airport_full_info[tujuan]}

                    Rute Optimal :

                    {' ➜ '.join(path)}

                    Jumlah Transit :
                    {max(0, len(path)-2)}

                    Total Biaya :
                    Rp {cost:,}
                    """)

                    # =====================
                    # JALUR
                    # =====================

                    st.subheader("🛫 Timeline Perjalanan")

                    for i, kode in enumerate(path):

                        if i == 0:
                            st.success(
                                f"🟢 Asal : {airport_full_info[kode]}"
                            )

                        elif i == len(path) - 1:
                            st.error(
                                f"🔴 Tujuan : {airport_full_info[kode]}"
                            )

                        else:
                            st.warning(
                                f"🟡 Transit {i} : {airport_full_info[kode]}"
                            )

                    st.divider()

                    # =====================
                    # DETAIL
                    # =====================

                    st.info(
                        f"💰 Total biaya seluruh perjalanan: Rp {cost:,}"
                    )

                    tab1, tab2, tab3 = st.tabs([
                        "💰 Detail Biaya",
                        "📋 Detail Jalur",
                        "📄 Export PDF"
                    ])

                    with tab1:
                        st.subheader("Detail Biaya Per Segmen")
                        segment_df = pd.DataFrame(segment_details)
                        segment_df["Harga"] = segment_df["Harga"].apply(
                            lambda x: f"Rp {x:,}"
                        )
                        st.dataframe(
                            segment_df,
                            use_container_width=True
                        )

                    with tab2:

                        st.subheader("Detail Jalur")

                        detail_df = pd.DataFrame({
                            "Kode Bandara": path,
                            "Nama Bandara": [
                                airport_dict[kode]
                                for kode in path
                            ],
                            "Kota": [
                                airport_city[kode]
                                for kode in path
                            ]
                        })

                        st.dataframe(
                            detail_df,
                            use_container_width=True
                        )

                    with tab3:

                        st.subheader("📄 Download Laporan PDF")

                        pdf_file = generate_pdf(
                            airport_full_info[asal],
                            airport_full_info[tujuan],
                            path,
                            cost,
                            total_distance
                        )

                        with open(pdf_file, "rb") as file:

                            st.download_button(
                                label="📄 Download PDF",
                                data=file,
                                file_name="hasil_rute.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                    st.divider()

                    st.markdown(
                        '<div class="sky-footer">Flight Route Finder Indonesia © 2026 | Algoritma Dijkstra</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {e}"
                    )

        else:

            st.info(
                "Silakan pilih bandara asal dan tujuan, kemudian klik tombol Cari Rute."
            )