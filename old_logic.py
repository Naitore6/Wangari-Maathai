import requests
import pandas as pd


# --- CONFIGURATION ---
# Set this to True because Java is currently down
USE_MOCK_DATA = True

# Java Config (Even though it's mocking, keep these ready)
JAVA_BASE_URL = "http://localhost:9090"
USERNAME = "0114440783" 
PASSWORD = "admin"

# MOCK DATA STORE
# This simulates what the Java Backend WOULD return if it was working
MOCK_REPORTS_JSON = [
    {
        "id": 101,
        "contact": "0700111222",
        "location": "Mau Complex - Block A",
        "description": "Saw fresh signs of illegal charcoal pits and 3 people fleeing.",
        "originalMessage": "Logging near Mau",
        "incidentType": "Charcoal Burning",
        "credibilityScore": 9.2,
        "createdOn": "2025-11-18T18:00:00"
    },
    {
        "id": 102,
        "contact": "0700333444",
        "location": "Karura Forest",
        "description": "Saw a vehicle without KFS registration carrying wood.",
        "originalMessage": "Truck with wood",
        "incidentType": "Illegal Logging",
        "credibilityScore": 7.5,
        "createdOn": "2025-11-18T19:00:00"
    },
    {
        "id": 103,
        "contact": "0700555666",
        "location": "Aberdare Hills",
        "description": "Possible poaching activity near the river crossing.",
        "originalMessage": "Poaching near river",
        "incidentType": "Poaching",
        "credibilityScore": 6.0,
        "createdOn": "2025-11-17T11:00:00"
    },
    {
        "id": 104,
        "contact": "0722000000",
        "location": "Karura Forest",
        "description": "Fencing broken near gate C",
        "originalMessage": "Broken fence",
        "incidentType": "Encroachment",
        "credibilityScore": 5.5,
        "createdOn": "2025-11-18T12:00:00"
    },
    {
        "id": 999,
        "contact": "0722000000",
        # Simulating a WhatsApp Location Pin
        "location": "-1.2921, 36.8219", 
        "description": "I am standing right next to the illegal logging site.",
        "originalMessage": "Location shared",
        "incidentType": "Illegal Logging",
        "credibilityScore": 9.5,
        "createdOn": "2025-11-19T10:00:00"
    }
]



class JavaConnector:
    def __init__(self):
        self.token = None

    def login(self):
        """Authenticates with Java Backend"""
        url = f"{JAVA_BASE_URL}/api/token"
        payload = { "username": USERNAME, "password": PASSWORD }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.token = response.json().get("token")
                print("Login Successful. Token acquired.")
                return True
            else:
                print(f"Login Failed: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"Connection Error: Is Java running at {JAVA_BASE_URL}?")
            return False 
            
    def get_reports(self):
        """Fetches reports, using mock data if the flag is set."""
        
        # 1. HANDLE MOCK DATA (The Bypass)
        if USE_MOCK_DATA:
            print("USING MOCK DATA (Java Backend Bypassed)")
            # Convert the list defined in Cell 2 to a DataFrame directly
            return pd.DataFrame(MOCK_REPORTS_JSON) 

        # 2. REAL LOGIC (Only runs if USE_MOCK_DATA is False)
        if not self.token:
            if not self.login():
                return pd.DataFrame()

        url = f"{JAVA_BASE_URL}/api/reports"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return pd.DataFrame(response.json())
            elif response.status_code == 401:
                print("Token expired. Refreshing...")
                self.login()
                return self.get_reports()
            else:
                print(f"Fetch Failed: {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()
        


def calculate_analytics():
    connector = JavaConnector()
    df = connector.get_reports()

    if df.empty:
        return {"error": "No data available"}

    # --- CLEANING ---
    if 'incidentType' in df.columns:
        df['incidentType'] = df['incidentType'].fillna("Unknown")
    
    if 'location' in df.columns:
        df['location'] = df['location'].fillna("Unspecified")

    # --- METRICS ---
    hotspots = df['location'].value_counts().head(5).to_dict()
    crime_stats = df['incidentType'].value_counts().to_dict()
    
    # Select specific columns for the 'Recent Reports' table
    # We check if columns exist first to avoid errors
    cols = ['id', 'incidentType', 'location', 'description', 'createdOn', 'credibilityScore']
    available_cols = [c for c in cols if c in df.columns]
    
    recent_reports = df[available_cols].tail(10).to_dict(orient='records')

    return {
        "summary": {
            "total_reports": len(df),
            "verified_reports": len(df[df['credibilityScore'] > 7]) if 'credibilityScore' in df.columns else 0
        },
        "hotspots": hotspots,
        "crime_stats": crime_stats,
        "recent_reports": recent_reports
    }

# Run the analytics function
result = calculate_analytics()

# Print the result beautifully
import json
print(json.dumps(result, indent=4))