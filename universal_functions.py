from typing import List
import csv
import sys
import json
from bson import json_util
import gridfs
from dotenv import load_dotenv
import os
import pymongo as pm


CATEGORIES = ['Immigration','Islamophobia','Transphobia','Anti-semitism']
COLLECTION_CONV = {'HL':'FarLeft',
                         'FR':'FarRight',
                         'CE19':'Center',
                         'CL19': 'CenterLeft',
                         "RR19": 'Right',
                         'CR19': 'CenterRight',
                         'CO':'FarRight','LL19':'Left','HR':'FarRight'}

def manage_overflow():
    # Manages overflow from importing .csv files with lots of text data in one column
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

def import_csv(csv_file:str)->List[List]:
    # Given a file location, imports the data as a nested list, each row is a new list
    manage_overflow() # manage overflow from large lines
    nested_list = []  # initialize list
    with open(csv_file, newline='', encoding='utf-8') as csvfile:  # open csv file
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            nested_list.append(row)  # add each row of the csv file to a list

    return nested_list


def export_nested_list(csv_name:str, nested_list:List[List]):
    # Export a nested list as a csv with a row for each sublist
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)

def export_list(csv_name:str, data_item:list):
    # Export a single list as a csv with one row
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data_item)

def export_as_json(export_filename:str, output):
    if export_filename.endswith('.json') is not True:
        raise Exception(f"{export_filename} should be a .json file")
    try:
        with open(export_filename, "w") as outfile:
            outfile.write(json.dumps(output))
    except TypeError:
        with open(export_filename, "w") as outfile:
            outfile.write(json_util.dumps(output))

def getConnection(
    connection_string: str = "", database_name: str = "", use_dotenv: bool = False
):
    "Returns MongoDB and GridFS connection"

    # Load config from config file
    if use_dotenv:
        load_dotenv()
        connection_string = os.getenv("CONNECTION_STRING")
        database_name = os.getenv("DATABASE_NAME")

    # Use connection string
    conn = pm.MongoClient(connection_string)
    db = conn[database_name]
    fs = gridfs.GridFS(db)

    return fs, db

def import_json(file):
    with open(file, 'r') as j:
        content = json.loads(j.read())
    return content



def remove_duplicates(data:list)->list:
    new_list  =[]
    for elt in data:
        if elt not in new_list:
            new_list.append(elt)
    return new_list
