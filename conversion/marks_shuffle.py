import pandas as pd

def marks_sort(sections, remainder, students, total_students, marks, students_df):
    div1 = students_df.loc[(students_df['Marks'] >= marks[0][0]) & (students_df['Marks'] < marks[0][1])].reset_index(drop=True)
    div2 = students_df.loc[(students_df['Marks'] >= marks[1][0]) & (students_df['Marks'] < marks[1][1])].reset_index(drop=True)
    div3 = students_df.loc[(students_df['Marks'] >= marks[2][0]) & (students_df['Marks'] < marks[2][1])].reset_index(drop=True)
    div4 = students_df.loc[(students_df['Marks'] >= marks[3][0]) & (students_df['Marks'] < marks[3][1])].reset_index(drop=True)
    div5 = students_df.loc[(students_df['Marks'] >= marks[4][0]) & (students_df['Marks'] < marks[4][1])].reset_index(drop=True)
    div6 = students_df.loc[(students_df['Marks'] >= marks[5][0]) & (students_df['Marks'] < marks[5][1])].reset_index(drop=True)

    marks_ratios = []

    start_index = 0
    for i in range(sections):
        end_index = start_index + students

        if i < remainder:
            end_index += 1

        diff = end_index - start_index

        div1_num = round((len(div1) / total_students) * diff)
        div2_num = round((len(div2) / total_students) * diff)
        div3_num = round((len(div3) / total_students) * diff)
        div4_num = round((len(div4) / total_students) * diff)
        div5_num = round((len(div5) / total_students) * diff)
        div6_num = round((len(div6) / total_students) * diff)

        marks_ratios.append((div1_num, div2_num, div3_num, div4_num, div5_num, div6_num))

    df = pd.DataFrame()
    for i in range(sections):
        partition = pd.concat([
            div1.iloc[:marks_ratios[i][0]],
            div2.iloc[:marks_ratios[i][1]],
            div3.iloc[:marks_ratios[i][2]],
            div4.iloc[:marks_ratios[i][3]],
            div5.iloc[:marks_ratios[i][4]],
            div6.iloc[:marks_ratios[i][5]],
        ]).sort_values(by=['2NDL']).reset_index(drop=True)

        df = pd.concat([df, partition]).reset_index(drop=True)

        div1 = div1.iloc[marks_ratios[i][0]:]
        div2 = div2.iloc[marks_ratios[i][1]:]
        div3 = div3.iloc[marks_ratios[i][2]:]
        div4 = div4.iloc[marks_ratios[i][3]:]
        div5 = div5.iloc[marks_ratios[i][4]:]
        div6 = div6.iloc[marks_ratios[i][5]:]

    combined_df = pd.concat([df, students_df]).reset_index(drop=True)
    df_groupby = combined_df.groupby(list(combined_df.columns))
    idx = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
    remaining = combined_df.reindex(idx)
    df = pd.concat([df, remaining]).reset_index(drop=True)

    return df

