from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logic

app = FastAPI(title="Wangari Maathai Analytics Middleware")

# Allow the UI to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System Health"])
def health_check():
    return {"status": "Online", "mode": "Mock Data Mode" if logic.USE_MOCK_DATA else "Live Production Mode"}

@app.get("/api/v1/dashboard-stats", tags=["Dashboard Analytics"])
def get_dashboard_stats():
    """
    Returns the analytics JSON for the Admin Dashboard
    """
    return logic.calculate_analytics()

@app.get("/api/v1/map-data", tags=["Map Data"])
def get_map_data():
    """
    Returns clean lat/lon data for the map
    """
    # We can reuse the same connector logic
    connector = logic.JavaConnector()
    df = connector.get_reports()
    
    if df.empty:
        return []

    map_points = []
    # Basic logic to extract coordinates if they exist in 'location' string
    if 'location' in df.columns:
        for _, row in df.iterrows():
            loc = str(row['location'])
            # If mock data has coordinates like "-1.2, 36.8"
            if "," in loc and any(c.isdigit() for c in loc):
                try:
                    lat, lon = loc.split(",")
                    map_points.append({
                        "lat": float(lat), 
                        "lon": float(lon), 
                        "desc": row.get('incidentType', 'Incident')
                    })
                except:
                    continue
    return map_points