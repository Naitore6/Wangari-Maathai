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