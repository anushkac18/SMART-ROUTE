# 🚌 Smart Route Recommendation System — India

Find the best bus/public-transit routes **in India** between two points.  
Optimizes for:
- **Fastest** travel time
- **Lowest Fare (₹)**
- **Least Crowded** (heuristic)

Uses **Google Maps Directions API (Transit)** if a key is provided; otherwise falls back to a small mock network (BMTC/BEST/DTC).

## 🚀 Setup Instructions

1. Clone or download this repo.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
