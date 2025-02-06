#!/usr/bin/python3

import json
from glob import glob


locations = set()

for file in glob("datasets/*.json"):
    with open(file, "r") as f:
        data = json.loads(f.read())

    for course in data:

        if course["LOCATIONS"] != None and course["SCHD_TYPE"] == "Lec":

            # Validates the maximum enrollment amount
            if "MAX_ENRL" not in course:
                print(f"Course excluded from the list for not including maximum enrollment: {course['CRSE_TITLE']}")
                continue

            max_enrollment = 0

            try:
                max_enrollment = int(course["MAX_ENRL"])
            except:
                # Handling for int parsing error
                print(f"Course excluded from the list for not having an integer maximum enrollment: {course['CRSE_TITLE']}")
                continue

            if max_enrollment <= 50:
                print(f"Course excluded from the list for not having large enough maximum enrollment: {course['CRSE_TITLE']}")
                continue

            multi_locations = []
            for location in course["LOCATIONS"].split("<br>"):

                if location.find("<") != -1 or location.find(">") != -1: continue

                # Basically `.contains()`
                if location.find(", ") != -1:
                    location = location.split(", ")
                    building = list(location.pop(0).split(" "))
                    location.append(building.pop(-1))
                    building = " ".join(building)

                    for room in location:
                        locations.add(f"{building} {room}")

                else: locations.add(location)
            continue;

        else: print(f"Course excluded from list: {course["CRSE_TITLE"]}")

with open("locations.txt", "w") as f:
    locations = list(locations)
    locations.sort()
    for location in locations:
        f.write(str(location) + "\n")
