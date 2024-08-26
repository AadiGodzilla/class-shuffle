import pandas as pd
import math
import os

from conversion.gender_shuffle import gender_sort
from conversion.houses_shuffle import house_sort
from conversion.secondlang_shuffle import second_lang_sort
from conversion.thirdlang_shuffle import third_lang_sort
from conversion.marks_shuffle import marks_sort

def conversion(class_name, sections, file):
    spreadsheet = pd.read_excel(file)

    genders = ['M', 'F']
    houses = ['A', 'D', 'G', 'K']
    second_langs = ["Nepali", "Hindi"]
    third_langs = ['N', 'H', 'F']
    marks = [(90, 100), (80, 90), (70, 80), (60, 70), (50, 60), (33, 50)]

    counter = 0
    dfs = {}

    for gender in genders:
        for house in houses:
            for second_lang in second_langs:
                for third_lang in third_langs:
                    for mark in marks:
                        mask = (
                            (spreadsheet['G'] == gender) &
                            (spreadsheet['H'] == house) &
                            (spreadsheet['2NDL'] == second_lang) &
                            (spreadsheet['3RDL'] == third_lang) &
                            (spreadsheet['Marks'] >= mark[0]) &
                            (spreadsheet['Marks'] < mark[1])
                        )
                        dfs[counter] = spreadsheet[mask]
                        counter += 1

    df = pd.concat(dfs.values(), ignore_index=True)
    df = df.sample(frac=1, random_state=42).sort_values(by=['NAME']).reset_index(drop=True)

    students = len(df) // sections
    remainder = len(df) % sections

    df = gender_sort(sections, remainder, students, genders, df)
    df = third_lang_sort(sections, remainder, students, len(df), third_langs, df)
    df = house_sort(sections, remainder, students, len(df), houses, df)
    df = marks_sort(sections, remainder, students, len(df), marks, df)
    df = second_lang_sort(sections, remainder, students, second_langs, df)

    print(df.to_string())

    try:
        os.mkdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "class", class_name)))
    except FileExistsError:
        pass

    start_index = 0
    char = 65
    for i in range(sections):
        end_index = start_index + students

        if i < remainder:
            end_index += 1

        partition = pd.DataFrame()
        partition = pd.concat([partition, df.iloc[start_index: end_index]]).reset_index(drop=True)

        roll_nos = partition['ROLL NO.']

        new_rolls = []
        for j in range(len(roll_nos)):
            class_roll = math.floor(roll_nos.iloc[j] / 1000) * 1000
            p = 1001 + ((100 * i) + j)
            class_roll += p
            new_rolls.append(class_roll)

        partition['ROLL NO.'] = new_rolls

        partition.to_excel(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "class", class_name, f"section_{chr(char)}.xlsx")), index=False)
        char += 1

        start_index = end_index
