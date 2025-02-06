#!/usr/bin/python3

import json
from glob import glob


locations = set()

for file in glob("datasets/*.json"):
    with open(file, "r") as f:
        data = json.loads(f.read())

    for course in data:
        if course["LOCATIONS"] != None and course["SCHD_TYPE"] == "Lec":

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

        else:
            print(f"Course excluded from list: {course["CRSE_TITLE"]}")

with open("locations.txt", "w") as f:
    locations = list(locations)
    locations.sort()
    for location in locations:
        f.write(str(location) + "\n")
