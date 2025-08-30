import os
import streamlit as st
import pandas as pd
import googlemaps
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

gmaps = None
if API_KEY:
    gmaps = googlemaps.Client(key=API_KEY)

st.set_page_config(page_title="Smart Route Finder India", page_icon="🚌", layout="centered")
st.title("🚌 Smart Route Recommendation System — India")

source = st.text_input("Enter Source:")
destination = st.text_input("Enter Destination:")
preference = st.selectbox("Optimization Preference", ["Fastest", "Lowest Fare (₹)", "Least Crowded"])

if st.button("Find Routes"):
    if source and destination:
        results = []
        if gmaps:
            try:
                now = datetime.now()
                directions = gmaps.directions(
                    source, destination, mode="transit", departure_time=now, region="in", alternatives=True
                )
                for d in directions:
                    leg = d['legs'][0]
                    duration = leg['duration']['value'] // 60
                    desc = f"{leg['start_address']} → {leg['end_address']}"
                    fare = d.get("fare", {"value": 30, "currency": "INR"})
                    crowd = "medium"
                    results.append({
                        "Route": desc,
                        "Time (min)": duration,
                        "Fare": f"₹{fare['value']}",
                        "Crowd": crowd
                    })
            except Exception as e:
                st.error(f"Google Maps API Error: {e}")
        else:
            # Mock routes for India if API not available
            results = [
                {"Route": "Majestic → Indiranagar", "Time (min)": 35, "Fare": "₹25", "Crowd": "high"},
                {"Route": "Majestic → Whitefield", "Time (min)": 55, "Fare": "₹40", "Crowd": "medium"},
                {"Route": "Majestic → Electronic City", "Time (min)": 65, "Fare": "₹50", "Crowd": "low"},
            ]

        if results:
            if preference == "Fastest":
                best = min(results, key=lambda x: x["Time (min)"])
            elif preference == "Lowest Fare (₹)":
                best = min(results, key=lambda x: int(x["Fare"].replace("₹", "")))
            else:
                crowd_rank = {"low": 1, "medium": 2, "high": 3}
                best = min(results, key=lambda x: crowd_rank[x["Crowd"]])

            st.success(f"✅ Best Route: {best['Route']}")
            st.write(f"🕒 Time: {best['Time (min)']} min")
            st.write(f"💸 Fare: {best['Fare']}")
            st.write(f"👥 Crowd: {best['Crowd']}")

            st.subheader("All Options")
            st.dataframe(pd.DataFrame(results))
        else:
            st.error("❌ No routes found")
    else:
        st.warning("Please enter both source and destination")
