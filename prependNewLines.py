#!/usr/bin/python3
import os
import sys
import csv
from typing import List
from typing import Dict
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilenames

def prepend_newlines(filepath, n):
    print(f"Prepending the file {filepath} with {n} lines.")
    with open(filepath, 'r') as original: data = original.read()
    with open(filepath, 'w') as modified: modified.write("\n"*n + data)

def ensure_dir(file_path: str):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_files():
    inputFiles = askopenfilenames(initialdir=os.getcwd(), title='Please select the input files')
    if isinstance(inputFiles, List) and not inputFiles:
        print('No valid input files have been chosen. Exiting!')
        exit()
    return inputFiles

def get_file(dir: str, file: str):
    return os.path.join(os.path.abspath(dir), file).replace('\\', '/')

def main():
    root = tk.Tk()
    root.withdraw()

    if not len(sys.argv) == 2:
        print("Usage: python3 prependNewLines.py <number of newlines to add>")
        print("Afterwards choose the files you want to prepend with the given amount of newlines")
        exit()
    n = int(sys.argv[1])

    inputFiles = get_files()
    file_count = 0
    for input_file in inputFiles:
        if os.path.isfile(input_file) and input_file.endswith(".csv"):
            print(f"Working on file: {input_file}")
            prepend_newlines(input_file, n)
            file_count += 1
    if file_count == 0:
        print('Are you in the correct directoy? 0 files have been processed. Exiting!')
    else:
        print(f'All of the {file_count} .csv files have been processed! Exiting!')
    exit()

main()