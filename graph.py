# ==============================
# CAMPUS GRAPH 
# ==============================

graph = {
    "Campus Center": [("Main Library", 2), ("Admin Office", 3), ("Learning Area", 2), ("Café", 2)],

    "Main Library": [("Female Library", 1), ("Digital Library", 2)],
    "Female Library": [("Digital Library", 1)],
    "Digital Library": [],

    "Admin Office": [("HR Office", 1), ("Freshman Office", 2), ("Staff Lounge", 2)],
    "HR Office": [("Freshman Office", 1)],
    "Freshman Office": [],

    "Learning Area": [("LH01", 1), ("CL01", 2), ("Male Lounge", 2)],
    "LH01": [("LH02", 1)],
    "LH02": [("LH03", 1)],
    "LH03": [("LH04", 1)],
    "LH04": [("Physics Lab", 2)],

    "CL01": [("CL02", 1)],
    "CL02": [("CL03", 1)],
    "CL03": [("CL04", 1)],
    "CL04": [],

    "Physics Lab": [("Chemistry Lab", 2)],
    "Chemistry Lab": [("Biology Lab", 2)],
    "Biology Lab": [("Sports Center", 3)],

    "Sports Center": [],

    # ==============================
    # NEW ADDITIONS (LOUNGES + CAFE)
    # ==============================

    "Café": [
        ("Campus Center", 2),
        ("Male Lounge", 1),
        ("Female Lounge", 1),
        ("Staff Lounge", 2)
    ],

    "Male Lounge": [
        ("Learning Area", 2)
    ],

    "Female Lounge": [
        ("Main Library", 2)
    ],

    "Staff Lounge": [
        ("Admin Office", 2)
    ]
}