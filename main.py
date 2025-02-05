#!/usr/bin/python3

import json
import base64
import requests
import random
from urllib.parse import *

with open("subjects.json", "r") as f:
    data = json.loads(f.read())

def fuck_ass_url_to_basic_params(url: str):
    # print("Parsing Stuff")
    parser = urlparse(url)

    # We get all the sections of the request
    params_lst = parser.query.split("&")
    all_values = {}

    for val in params_lst:

        values = []
        out_word = ""
        is_equal_sign = False

        for char_idx in range(len(val)):
            if val[char_idx] != "=" and is_equal_sign:
                values.append(out_word)
                out_word = ""
                is_equal_sign = False
            out_word += val[char_idx]

            if val[char_idx] == "=":
                is_equal_sign = True

            if char_idx == len(val) - 1:
                values.append(out_word)

        # print(values)
        if len(values) == 2:
            values[0] = values[0].strip("=")
        elif len(values) == 4:
            values[0] = base64.b64decode(values[1])
            if values[3] == "null" or values[3] == "undefined":
                values[1] = values[3]
            else:
                values[1] = base64.b64decode(values[3])
            values.pop(3)
            values.pop(2)
        else:
            print(f"Warning: Unexpected length value: {len(values)}")

        all_values[values[0]] = values[1]

    # print("Params: " + str(all_values))
    return all_values

def params_to_fuck_ass_url(data: dict[str, str]) -> dict[str, str]:
# def params_to_fuck_ass_url(data: dict[str, str]) -> str:
    out_data = {}
    out_str = ""

    for (k, v) in data.items():

        if type(k) == bytes: k = str(k, "utf-8")
        if type(v) == bytes: v = str(v, "utf-8")

        key = str(base64.b64encode(str(get_random_arbitrary()).encode("utf-8")), "utf-8") + str(base64.b64encode(k.encode("utf-8")), "utf-8")
        if v == "null" or v == "undefined" or v == None:
            value = v
        else:
            value = str(base64.b64encode(str(get_random_arbitrary()).encode("utf-8")), "utf-8") + str(base64.b64encode(v.encode("utf-8")), "utf-8")
        out_data[key] = value
        out_str += key + value + "&"

    out_str += "encoded=true"
    out_str.strip("&")
    out_data["encoded"] = "true"

    # return out_str
    return out_data

def get_random_arbitrary(min: int = 0, max: int = 99):
    return int(random.random() * (max - min) + min)

def get_academic_time_table(cookie: dict[str, str], year: int) -> str:
    terms = "".join(f"{year}{i}{0};" for i in range(0, 4))
    params = params_to_fuck_ass_url({"districts": "100;200;300;400;", "terms": terms})
    url = "https://self-service.dal.ca/BannerExtensibility/internalPb/virtualDomains.dal_stuweb_academicTimetable_subjects";
    return requests.get(url, headers=headers, params=params, cookies=cookie).text

# Requesting courses
# fuck_ass_url_to_basic_params("https://self-service.dal.ca/BannerExtensibility/internalPb/virtualDomains.dal_stuweb_academicTimetable?MTM=b2Zmc2V0=NTQ=MA==&MTg=bWF4=OTk=MTAwMA==&MjM=ZGlzdHJpY3Rz=OA==MTAwOzIwMDszMDA7NDAwOw==&MzU=Y3JzZV9udW1i=NjA=null&MzU=cGFnZV9zaXpl=NDM=OTk5OQ==&NDQ=dGVybXM==MTg=MjAyNTAwOzIwMjUxMDsyMDI1MjA7MjAyNTMwOw==&NjA=c3Vial9jb2Rl=Mzg=Q1NDSQ==&Njg=cGFnZV9udW0==NjE=MQ==&encoded=true")
# Getting the dataset
# fuck_ass_url_to_basic_params("https://self-service.dal.ca/BannerExtensibility/internalPb/virtualDomains.dal_stuweb_academicTimetable_subjects?NA==dGVybXM==Nzk=MjAyNTMwOzIwMjUyMDsyMDI1MTA7MjAyNTAwOw==&OQ==ZGlzdHJpY3Rz=NTg=MTAwOzIwMDszMDA7NDAwOw==&encoded=true")
# print(get_academic_time_table(cookie, 2025))

cookie = input("Enter your browser cookie from `https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable`: ")
cookie = {"JSESSIONID": cookie}

headers = {
    "Host": "self-service.dal.ca",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Referer": "https://self-service.dal.ca/BannerExtensibility/customPage/page/dal.stuweb_academicTimetable",
}


