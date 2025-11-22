import requests
import pandas as pd
import os
import mock_data  # fecth mock_data.py file in the same folder

# --- CONFIGURATION ---
# Get the Java URL from the Environment (Render) OR default to Localhost
JAVA_BASE_URL = os.environ.get("JAVA_API_URL", "http://localhost:9090")

# Mock Data Switch
# check the environment variable. If missing, default to False.
use_mock_str = os.environ.get("USE_MOCK_DATA", "False")
USE_MOCK_DATA = use_mock_str.lower() == "true"

# Credentials, Using those in the db
USERNAME = os.environ.get("ADMIN_USERNAME", "0114440780")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

class JavaConnector:
    def __init__(self):
        self.token = None

    def login(self):
        """Authenticates with Java Backend"""
        url = f"{JAVA_BASE_URL}/api/token"
        payload = {"username": USERNAME, "password": PASSWORD}
        
        try:
            response = requests.post(url, json=payload, timeout=5) # 5 second timeout
            if response.status_code == 200:
                self.token = response.json().get("token")
                print("Login Successful. Token acquired.")
                return True
            else:
                print(f"Login Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Login Connection Failed: {e}")
            return False

    def get_reports(self):
        """
        Fetches reports with AUTOMATIC FALLBACK.
        1. Tries to fetch from Real Java Backend.
        2. If that fails (server down), automatically returns Mock Data.
        """
        
        # Attempt to get Real Data first
        try:
            # 1. Check if we have a token, if not, try to log in
            if not self.token:
                if not self.login():
                    raise ConnectionError("Could not log in to Backend")

            # 2. Make the Request
            url = f"{JAVA_BASE_URL}/api/reports"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Set a short timeout (e.g., 3 seconds) so the UI doesn't hang if Java is down
            response = requests.get(url, headers=headers, timeout=3)
            
            if response.status_code == 200:
                print("Serving REAL DATA from Java Backend")
                return pd.DataFrame(response.json())
            else:
                print(f"Backend returned error {response.status_code}, switching to Mock.")
                raise ConnectionError("Backend returned error status")

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, ConnectionError) as e:
            # --- THE SAFETY NET ---
            print(f"CONNECTION FAILED ({e}).")
            print("ACTIVATING CIRCUIT BREAKER: Serving MOCK DATA.")
            return pd.DataFrame(mock_data.MOCK_REPORTS_JSON)

# --- ANALYTICS FUNCTION ---
def calculate_analytics():
    connector = JavaConnector()
    df = connector.get_reports()

    if df.empty:
        return {"error": "No data available"}

    # --- CLEANING & ANALYTICS ---
    if 'incidentType' in df.columns:
        df['incidentType'] = df['incidentType'].fillna("Unknown")
    else:
        df['incidentType'] = "Unknown" # Handle mock data case if key missing
        
    if 'location' in df.columns:
        df['location'] = df['location'].fillna("Unspecified")
    else:
        df['location'] = "Unspecified"

    # Metrics
    hotspots = df['location'].value_counts().head(5).to_dict()
    crime_stats = df['incidentType'].value_counts().to_dict()
    
    # Recent Reports (Safe Column Selection)
    cols = ['id', 'incidentType', 'location', 'description', 'createdOn', 'credibilityScore']
    available_cols = [c for c in cols if c in df.columns]
    recent_reports = df[available_cols].tail(10).to_dict(orient='records')

    return {
        "summary": {
            "total_reports": len(df),
            # Safe check for verified column
            "verified_reports": len(df[df['credibilityScore'] > 7]) if 'credibilityScore' in df.columns else 0
        },
        "hotspots": hotspots,
        "crime_stats": crime_stats,
        "recent_reports": recent_reports
    }