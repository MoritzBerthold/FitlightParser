import os
import sys
import csv
from typing import List
from typing import Dict
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilenames
from FitlightExport import FitlightColumn
from FitlightExport import FitlightOutputColumn

def parseCSV(input_file, output_file):
    importedData = importData(input_file)
    exportData = dict()
    steps: Dict[str, FitlightColumn]
    for id1, steps in importedData.items():
        exportData[id1] = FitlightOutputColumn(steps.values())
    filtered = filterBestSectionTotal(exportData)
    export(filtered, output_file, FitlightOutputColumn.Columns)
    return

def filterBestSectionTotal(runs: Dict[str, FitlightOutputColumn]):
    result: Dict[str, FitlightOutputColumn] = dict()
    for run in runs.values():
        athleteName = run.getAthleteName()
        if athleteName not in result or result[athleteName].getSectionTotal() < run.getSectionTotal():
            result[athleteName] = run
    return result

def export(data: Dict[str, FitlightOutputColumn], out_path: str, out_fieldnames: List[str]):
    with open(out_path, 'w+', newline='') as out_file:
        writer = csv.DictWriter(
            out_file, fieldnames=out_fieldnames, delimiter=';')
        writer.writeheader()
        d: FitlightColumn
        for d in data.values():
            writer.writerow(d.Cells)

def importData(input_file: str):
    result = dict()
    with open(input_file, 'r', newline='') as in_file:
        reader = csv.DictReader(in_file, delimiter=';')
        if not set(FitlightColumn.Columns).issubset(set(reader.fieldnames)):
            print("Expected different headers. Skipping file!")
            return
        for row in reader:
            id1 = row[FitlightColumn.IdColumn1]
            id2 = row[FitlightColumn.IdColumn2]
            if id1 not in result:
                result[id1] = dict()
            result[id1][id2] = FitlightColumn(row)
    return result

def ensure_dir(file_path: str):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_directories():
    inputFiles = askopenfilenames(initialdir=os.getcwd(), title='Please select the input files')
    if isinstance(inputFiles, List) and not inputFiles:
        print('No valid input files have been chosen. Exiting!')
        exit()
    output_dir = askdirectory(mustexist=True, initialdir=os.getcwd(), title='Please select an output directory')
    if not os.path.isdir(output_dir):
        print('No valid output directory has been chosen. Exiting!')
        exit()
    return inputFiles, output_dir

def get_file(dir: str, file: str):
    return os.path.join(os.path.abspath(dir), file).replace('\\', '/')

def main():
    root = tk.Tk()
    root.withdraw()

    inputFiles, output_dir = get_directories()
    file_count = 0
    for input_file in inputFiles:
        if os.path.isfile(input_file) and input_file.endswith(".csv"):
            print(f"Working on file: {input_file}")
            name, ext = os.path.splitext(os.path.basename(input_file))
            output_file = get_file(output_dir, f"{name}_out{ext}")
            print(f"New data in file: {output_file}")
            parseCSV(input_file, output_file)
            file_count += 1
    if file_count == 0:
        print('Are you in the correct directoy? 0 files have been processed. Exiting!')
    else:
        print(f'All of the {file_count} .csv files have been processed! Exiting!')
    exit()

main()