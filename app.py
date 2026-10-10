import streamlit as st
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Project-Q: Disaster Allocation System", page_icon="🚨", layout="wide")

st.title("🚨 Project-Q: Smart Disaster Response & Logistics System")
st.markdown("### Powered by Weather Intelligence, GPS Routing & Quantum-Inspired Allocation")

# --- SIDEBAR: INPUT CONTROLS ---
st.sidebar.header("1. Meteorological Forecast")
wind_speed = st.sidebar.slider("Wind Speed (km/h)", 20, 200, 135)
rainfall = st.sidebar.slider("Rainfall (mm)", 10, 300, 180)
river_level = st.sidebar.slider(
    "River Water Level (m)",
    min_value=2.0,
    max_value=15.0,
    value=8.5,
    step=0.5
)

st.sidebar.header("2. Logistics & Warehouse Inventory")
total_meds = st.sidebar.number_input("Available Medical Kits", value=1000, step=50)
total_food = st.sidebar.number_input("Available Food Boxes", value=2500, step=50)

st.sidebar.header("3. Zone Damage & GPS Settings")
z1_pop = st.sidebar.slider("Zone Alpha Population", 1000, 20000, 5000)
z1_damage = st.sidebar.slider("Zone Alpha Damage (%)", 10, 100, 80) / 100.0
z1_blockage = st.sidebar.selectbox("Zone Alpha Road Status", ["Clear", "flooded_bridge", "landslide", "debris"], index=1)

z2_pop = st.sidebar.slider("Zone Beta Population", 1000, 20000, 3000)
z2_damage = st.sidebar.slider("Zone Beta Damage (%)", 10, 100, 40) / 100.0
z2_blockage = st.sidebar.selectbox("Zone Beta Road Status", ["Clear", "flooded_bridge", "landslide", "debris"], index=0)


# --- CORE LOGIC FUNCTIONS ---
def detect_disaster(wind, rain, river):
    if wind > 120 or rain > 150 or river > 8.0:
        return "Critical / Severe Cyclone-Flood Risk", "red"
    elif wind > 80 or rain > 80 or river > 5.0:
        return "Moderate Storm / Flood Warning", "orange"
    else:
        return "Normal / Safe Conditions", "green"

def calculate_shortest_route(warehouse_gps, disaster_gps, blockage):
    lat_diff = disaster_gps[0] - warehouse_gps[0]
    lon_diff = disaster_gps[1] - warehouse_gps[1]
    base_dist = np.sqrt(lat_diff**2 + lon_diff**2) * 111
    
    multiplier = 1.4 if blockage != "Clear" else 1.0
    final_dist = round(base_dist * multiplier, 2)
    est_time = round((final_dist / 40) * 60, 1)
    status = f"Detour Active ({blockage})" if blockage != "Clear" else "Clear Route"
    return final_dist, est_time, status

def allocate_emergency_kits(inventory, zones):
    total_damage_score = sum([d["population"] * d["damage_percentage"] for d in zones.values()])
    results = {}
    for name, data in zones.items():
        impact = data["population"] * data["damage_percentage"]
        share = impact / total_damage_score if total_damage_score > 0 else 0
        meds = int(inventory["medical_kits"] * share)
        food = int(inventory["food_boxes"] * share)
        results[name] = {"meds": meds, "food": food, "damage": int(data["damage_percentage"] * 100)}
    return results


# --- MAIN DASHBOARD INTERFACE ---
if st.button("🚀 Run Emergency Logistics Simulation"):
    
    # 1. Weather Module Output
    status_text, color = detect_disaster(wind_speed, rainfall, river_level)
    st.markdown(f"### ⛅ Weather Forecast Detection")
    st.markdown(f"<p style='font-size:20px; color:{color}; font-weight:bold;'>Status: {status_text}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # 2. GPS Routing Module Output
    st.markdown("### 🗺️ GPS Shortest Route Optimization")
    wh_gps = (17.3850, 78.4867) # Central Warehouse
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.subheader("📍 Zone Alpha Logistics")
        dist1, time1, r_status1 = calculate_shortest_route(wh_gps, (17.5000, 78.6000), z1_blockage)
        st.metric(label="Shortest Distance", value=f"{dist1} km")
        st.metric(label="Estimated Travel Time", value=f"{time1} mins")
        st.write(f"**Route Status:** {r_status1}")
        
    with col_r2:
        st.subheader("📍 Zone Beta Logistics")
        dist2, time2, r_status2 = calculate_shortest_route(wh_gps, (17.3000, 78.3000), z2_blockage)
        st.metric(label="Shortest Distance", value=f"{dist2} km")
        st.metric(label="Estimated Travel Time", value=f"{time2} mins")
        st.write(f"**Route Status:** {r_status2}")
        
    st.divider()
    
    # 3. Resource Allocation Output
    st.markdown("### 📦 Damage-Based Emergency Kit Allocation")
    inventory_dict = {"medical_kits": total_meds, "food_boxes": total_food}
    zones_dict = {
        "Zone Alpha": {"population": z1_pop, "damage_percentage": z1_damage},
        "Zone Beta": {"population": z2_pop, "damage_percentage": z2_damage}
    }
    
    allocations = allocate_emergency_kits(inventory_dict, zones_dict)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        z_a = allocations["Zone Alpha"]
        st.success(f"**Zone Alpha Allocation** ({z_a['damage']}% Impact)")
        st.write(f"💉 Medical Kits Sent: **{z_a['meds']}**")
        st.write(f"🍞 Food Boxes Sent: **{z_a['food']}**")
        
    with col_a2:
        z_b = allocations["Zone Beta"]
        st.info(f"**Zone Beta Allocation** ({z_b['damage']}% Impact)")
        st.write(f"💉 Medical Kits Sent: **{z_b['meds']}**")
        st.write(f"🍞 Food Boxes Sent: **{z_b['food']}**")
        
    st.balloons()
