import os
import django
import csv
import datetime
import tkinter as tk
from tkinter import filedialog

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SafeLab.settings')
django.setup()

from CPanel.models import Aparatu

def save_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row:
                aparatu = Aparatu()
                aparatu.name = row[0]
                aparatu.mark = row[1]
                aparatu.range = row[2]
                aparatu.cant = row[3]
                aparatu.Obsevation = row[4]
                aparatu.date = datetime.datetime.strptime(row[5], '%Y-%m-%d').date()
                aparatu.save()
    print("Data has been saved successfully")

def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title='Select CSV file', filetypes=[("CSV files", "*.csv")])


if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        print(f'Selected file: {file_path}')
        save_data_from_csv(file_path)
    else:
        print("No file was selected")            
