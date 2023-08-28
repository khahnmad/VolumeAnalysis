from typing import List
import csv

def export_nested_list(csv_name:str, nested_list:List[List]):
    # Export a nested list as a csv with a row for each sublist
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)
