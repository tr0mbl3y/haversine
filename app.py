import streamlit as st
import h3
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="H3 Driver Finder", layout="wide")

st.title("Find Nearby Drivers Using H3")
st.markdown("Enter pickup coordinates and adjust the resolution and search radius (K-ring) to see nearby drivers.")

# Sidebar inputs
with st.sidebar:
    st.header("Input Coordinates")
    lat = st.number_input("Latitude", value=23.0225, format="%.6f")
    lng = st.number_input("Longitude", value=72.5714, format="%.6f")

    st.header("Parameters")
    resolution = st.slider("H3 Resolution (0–15)", min_value=0, max_value=15, value=12)
    k = st.slider("Search Radius (K-Ring)", min_value=0, max_value=10, value=4)

# Dummy driver data (static)
drivers = [
    {"id": "Driver_1", "lat": lat + 0.0005, "lng": lng + 0.0004},
    {"id": "Driver_2", "lat": lat - 0.0007, "lng": lng - 0.0012},
    {"id": "Driver_3", "lat": lat + 0.0025, "lng": lng + 0.0025},
    {"id": "Driver_4", "lat": lat + 0.0100, "lng": lng + 0.0080},
    {"id": "Driver_5", "lat": lat - 0.0120, "lng": lng - 0.0100}
]

# H3 logic
pickup_cell = h3.latlng_to_cell(lat, lng, resolution)
nearby_hexes = h3.grid_disk(pickup_cell, k)

nearby_drivers = []
for driver in drivers:
    driver_cell = h3.latlng_to_cell(driver["lat"], driver["lng"], resolution)
    driver["cell"] = driver_cell
    if driver_cell in nearby_hexes:
        nearby_drivers.append(driver)

# Print results
st.subheader("Nearby Drivers")
st.markdown(f"Found **{len(nearby_drivers)}** driver(s) near pickup point ({lat}, {lng}):")
for d in nearby_drivers:
    st.write(f" {d['id']} at ({d['lat']:.5f}, {d['lng']:.5f})")

# Draw map
m = folium.Map(location=[lat, lng], zoom_start=14)

# Pickup marker
folium.Marker([lat, lng], tooltip="Pickup", icon=folium.Icon(color="red")).add_to(m)

# Driver markers
for driver in drivers:
    color = "green" if driver in nearby_drivers else "gray"
    folium.Marker(
        [driver['lat'], driver['lng']],
        tooltip=driver['id'],
        icon=folium.Icon(color=color)
    ).add_to(m)

# H3 hexagons
for hex_id in nearby_hexes:
    boundary = h3.cell_to_boundary(hex_id)
    folium.Polygon(
        locations=boundary,
        color="blue",
        fill=True,
        fill_opacity=0.2
    ).add_to(m)

# Show map in app
st.subheader("Nearby Area Hex View")
st_data = st_folium(m, width=900, height=600)
