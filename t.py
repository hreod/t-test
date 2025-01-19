import pandas as pd
import folium

# Завантаження даних із CSV
file_path = "buildings.csv"
data = pd.read_csv(file_path)

# Створення карти з топографічним базовим шаром
map_center = [51.675656, 39.131382]  # Центр міста Воронеж
my_map = folium.Map(location=map_center, zoom_start=12, tiles="OpenTopoMap", control_scale=True)

# Перебір даних
for _, row in data.iterrows():
    # Отримуємо координати центру будинку
    coords = list(map(float, row["coordinates"].split(',')))
    name = row["name"]
    floors = row["number of storeys"]
    address = row["address"]

    # Додаємо позначку на карту
    popup_text = (
        f"<b>Назва:</b> {name}<br>"
        f"<b>Адреса:</b> {address}<br>"
        f"<b>Кількість поверхів:</b> {floors}"
    )
    folium.Marker(
        location=coords,
        popup=popup_text,
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(my_map)

    # Створюємо область (силует будинку)
    offset = 0.00001 * floors  # Масштаб залежить від кількості поверхів
    polygon_coords = [
        [coords[0] - offset, coords[1] - offset],  # Лівий нижній
        [coords[0] - offset, coords[1] + offset],  # Лівий верхній
        [coords[0] + offset, coords[1] + offset],  # Правий верхній
        [coords[0] + offset, coords[1] - offset],  # Правий нижній
    ]
    folium.Polygon(
        locations=polygon_coords,
        color="red",
        fill=True,
        fill_color="orange",
        fill_opacity=0.4,
        tooltip=f"Силует будинку: {name}"
    ).add_to(my_map)

# Збереження карти
my_map.save("topographic_map_with_buildings.html")
