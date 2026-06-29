import streamlit as st
import folium
from streamlit_folium import st_folium
from graph.workflow import graph
from tools.reverse_geocode_tool import reverse_geocode
from streamlit_geolocation import streamlit_geolocation


st.set_page_config(
    page_title="AI Route Planner",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 AI Route Planner")

col1, col2 = st.columns([4, 1])

col1, col2 = st.columns([5, 1])

with col1:
    source = st.text_input(
        "📍 Source",
        value=st.session_state.get("source", "")
    )
if st.button("📡 Current"):
        st.session_state["get_location"] = True
with col2:
    st.write("")
    st.write("")

    
        

    if st.session_state.get("get_location", False):

            location = streamlit_geolocation()

            if location and location.get("latitude") is not None:

                lat = location["latitude"]
                lon = location["longitude"]

                address = reverse_geocode(lat, lon)

                st.session_state["source"] = address
                st.session_state["lat"] = lat
                st.session_state["lon"] = lon

                st.session_state["get_location"] = False

                st.rerun()

destination = st.text_input("🎯 Destination")


if st.button("🚀 Plan Route"):

    if not source.strip():
        st.error("Please enter a source.")
        st.stop()

    if not destination.strip():
        st.error("Please enter a destination.")
        st.stop()

    try:
        with st.spinner("Planning your trip..."):
            result = graph.invoke({
                "source": source,
                "destination": destination
            })
            decision = result["decision"]
            selected = decision["selected_route"] - 1
            chosen_route = result["route"]["routes"][selected]

            st.success(f"Recommended Route #{decision['selected_route']}")

            st.info(decision["reason"])

        st.session_state["result"] = result

    except Exception as e:
        st.exception(e)

coordinates=[]


if "result" in st.session_state:

    result = st.session_state["result"]
    decision = result["decision"]

    selected = decision["selected_route"] - 1
    chosen_route = result["route"]["routes"][selected]

    st.subheader("📋 AI Travel Report")
    st.markdown(result["report"])

    st.subheader("🛣 Available Routes")

    for route in result["route"]["routes"]:

        if route["route_id"] == decision["selected_route"]:
            st.success(f"⭐ Recommended Route {route['route_id']}")
        else:
            st.info(f"Route {route['route_id']}")

        st.write(f"📏 Distance: {route['distance_km']} km")
        st.write(f"⏱ Time: {route['travel_time_min']} min")
        st.write(f"🚦 Delay: {route['traffic_delay_min']} min")

        st.divider()

    coords = chosen_route["coordinates"]

    m = folium.Map(
        location=coords[0],
        zoom_start=12
    )

    folium.PolyLine(
        coords,
        weight=6,
        color="blue"
    ).add_to(m)

    folium.Marker(
        coords[0],
        tooltip="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        coords[-1],
        tooltip="Destination",
        icon=folium.Icon(color="red")
    ).add_to(m)

    if "lat" in st.session_state and "lon" in st.session_state:
        folium.Marker(
            [
                st.session_state["lat"],
                st.session_state["lon"]
            ],
            tooltip="Current Location",
            icon=folium.Icon(color="green", icon="home")
        ).add_to(m)

    st_folium(m, width=900, height=600)