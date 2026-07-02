import folium
from folium.plugins import PolyLineTextPath


def create_map(airports, path=None):

    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles=None
    )

    folium.TileLayer(
        "OpenStreetMap",
        name="OpenStreetMap"
    ).add_to(m)

    folium.TileLayer(
        "CartoDB Voyager",
        name="Voyager"
    ).add_to(m)

    folium.TileLayer(
        "CartoDB Positron",
        name="Positron"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # =========================
    # Marker Bandara
    # =========================
    for _, airport in airports.iterrows():

        popup_text = f"""
        <b>{airport['nama']}</b><br>
        Kode : {airport['kode']}<br>
        Kota : {airport['kota']}
        """

        folium.Marker(
            location=[
                airport["lat"],
                airport["lon"]
            ],
            popup=folium.Popup(
                popup_text,
                max_width=250
            ),
            tooltip=f"{airport['kode']} - {airport['nama']}",
            icon=folium.Icon(
                color="blue",
                icon="plane",
                prefix="fa"
            )
        ).add_to(m)

    # =========================
    # Jalur Hasil Dijkstra
    # =========================
    if path is not None and len(path) > 1:

        coordinates = []

        for code in path:

            airport_data = airports[
                airports["kode"] == code
            ]

            if not airport_data.empty:

                coordinates.append([
                    float(airport_data.iloc[0]["lat"]),
                    float(airport_data.iloc[0]["lon"])
                ])

        # Garis Putus-putus Merah
        folium.PolyLine(
            locations=coordinates,
            color="#FFBB00",
            weight=6,
            opacity=0.9,
            dash_array="10,10"
        ).add_to(m)

        # Marker Transit Berwarna Merah
        for i, coord in enumerate(coordinates):

            folium.CircleMarker(
                location=coord,
                radius=8,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=1,
                tooltip=f"Transit {i+1}"
            ).add_to(m)

        # Zoom otomatis ke jalur
        m.fit_bounds(coordinates)

    return m