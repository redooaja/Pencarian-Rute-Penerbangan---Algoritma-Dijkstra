def estimate_flight_time(total_distance):

    # Rata-rata kecepatan pesawat komersial
    average_speed = 800

    hours = total_distance / average_speed

    total_minutes = int(hours * 60)

    jam = total_minutes // 60
    menit = total_minutes % 60

    return f"{jam} Jam {menit} Menit"