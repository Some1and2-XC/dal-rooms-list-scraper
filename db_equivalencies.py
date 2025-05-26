#!/usr/bin/python3

import sqlite3
import os
import json
import re
from glob import glob

db_name = "dal.db"
db_exists = os.path.isfile(db_name)

con = sqlite3.connect("dal.db")
cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

if not db_exists:

    schema = """

CREATE TABLE IF NOT EXISTS Institutions (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Subject (
    subj_code TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Courses (
    subject TEXT REFERENCES Subject(subj_code) NOT NULL,
    code INTEGER NOT NULL,
    PRIMARY KEY (subject, code)
);

CREATE TABLE IF NOT EXISTS Equivalencies (
    subject TEXT NOT NULL,
    course_code INTEGER NOT NULL,
    ROW_NUMBER INTEGER NOT NULL,
    DE_INSTIT_CODE TEXT,
    DE_SUBJ_CODE TEXT,
    DE_CRSE_NUMBER TEXT,
    DE_FROM_CLASS TEXT,
    DE_FROM_CRE_HRS TEXT,
    DE_EQUV_SYMBOL TEXT,
    DE_TO_CLASS TEXT,
    DE_TO_HRS TEXT,
    DE_LAST_ASSESSED TEXT,
    OI_SUBJT_CODE TEXT,
    OI_CRSE_CODE TEXT,
    OI_INSTIT_CODE TEXT,
    OI_DAL_COURSE TEXT,
    OI_DAL_CRE_HRS TEXT,
    OI_EQUV_SYMBOL TEXT,
    OI_INSTITUTION REFERENCES Institutions(name),
    OI_INSTIT_EQUV TEXT,
    OI_INSTIT_CRE_HRS TEXT,
    OI_LAST_ASSESSED TEXT,
    INFO_TEXT TEXT,
    PRIMARY KEY(subject, course_code, ROW_NUMBER),
    FOREIGN KEY(subject, course_code) REFERENCES Courses(subject, code)
);
    """

    for rule in schema.split(";"):
        cur.execute(rule)

    con.commit()

files = glob("equivalencies/*.json")
files.sort(reverse=True)

for file in files:

    match = re.match("equivalencies/([A-Z]{4})-([0-9]{4}).json", file)
    assert(match)
    subject = match.group(1)
    course_number = match.group(2)

    try:
        cur.execute("INSERT INTO Subject (subj_code) VALUES (?)", (subject,))
    except:
        ...
    try:
        cur.execute("INSERT INTO Courses (subject, code) VALUES (?, ?)", (subject, course_number))
    except Exception as e:
        # print(f"Failed to add course (likely already exists for {file}). Error: {e}.")
        ...

    with open(file, "r") as f:
        data = json.loads(f.read())
        for entry in data:
            institution = entry["OI_INSTITUTION"]
            if institution is not None:
                try:
                    cur.execute("INSERT INTO Institutions (name) VALUES (?)", (institution,))
                except:
                    ...

            if "ROW_NUMBER" not in entry:
                # print(f"WARNING: Row number not specified in {file} somewhere. Skipping...")
                continue

            try:
                cur.execute(
                    """
                    INSERT INTO Equivalencies (
                        subject,
                        course_code,
                        ROW_NUMBER,
                        DE_INSTIT_CODE,
                        DE_SUBJ_CODE,
                        DE_CRSE_NUMBER,
                        DE_FROM_CLASS,
                        DE_FROM_CRE_HRS,
                        DE_EQUV_SYMBOL,
                        DE_TO_CLASS,
                        DE_TO_HRS,
                        DE_LAST_ASSESSED,
                        OI_SUBJT_CODE,
                        OI_CRSE_CODE,
                        OI_INSTIT_CODE,
                        OI_DAL_COURSE,
                        OI_DAL_CRE_HRS,
                        OI_EQUV_SYMBOL,
                        OI_INSTITUTION,
                        OI_INSTIT_EQUV,
                        OI_INSTIT_CRE_HRS,
                        OI_LAST_ASSESSED,
                        INFO_TEXT)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        subject,
                        course_number,
                        entry["ROW_NUMBER"],
                        entry["DE_INSTIT_CODE"],
                        entry["DE_SUBJ_CODE"],
                        entry["DE_CRSE_NUMBER"],
                        entry["DE_FROM_CLASS"],
                        entry["DE_FROM_CRE_HRS"],
                        entry["DE_EQUV_SYMBOL"],
                        entry["DE_TO_CLASS"],
                        entry["DE_TO_HRS"],
                        entry["DE_LAST_ASSESSED"],
                        entry["OI_SUBJT_CODE"],
                        entry["OI_CRSE_CODE"],
                        entry["OI_INSTIT_CODE"],
                        entry["OI_DAL_COURSE"],
                        entry["OI_DAL_CRE_HRS"],
                        entry["OI_EQUV_SYMBOL"],
                        entry["OI_INSTITUTION"],
                        entry["OI_INSTIT_EQUV"],
                        entry["OI_INSTIT_CRE_HRS"],
                        entry["OI_LAST_ASSESSED"],
                        entry["INFO_TEXT"],
                    )
                )

            except Exception as e:
                row = entry["ROW_NUMBER"]
                print(f"Failed to add value to database: {file} - row: {row}. Error: {e}")
        con.commit()

    con.commit()

