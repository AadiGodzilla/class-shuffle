import pandas as pd

def third_lang_sort(sections, remainder, students, total_students, third_langs, students_df):
    trd_nep_students = students_df.loc[students_df['3RDL'] == third_langs[0]]
    trd_hin_students = students_df.loc[students_df['3RDL'] == third_langs[1]]
    trd_fre_students = students_df.loc[students_df['3RDL'] == third_langs[2]]

    trd_lang_ratios = []

    start_index = 0
    for i in range(sections):
        end_index = start_index + students
        if i < remainder:
            end_index += 1

        diff = end_index - start_index

        trd_hin_students_ratio = int(round(float("{:.2f}".format(len(trd_hin_students) / total_students)) * diff))
        trd_nep_students_ratio = int(round(float("{:.2f}".format(len(trd_nep_students) / total_students)) * diff))
        trd_fre_students_ratio = int(round(float("{:.2f}".format(len(trd_fre_students) / total_students)) * diff))

        trd_lang_ratios.append((trd_hin_students_ratio, trd_nep_students_ratio, trd_fre_students_ratio))

        start_index = end_index

    df = pd.DataFrame()

    for i in range(sections):
        partition = pd.concat([
            trd_hin_students.iloc[:trd_lang_ratios[i][0]],
            trd_nep_students.iloc[:trd_lang_ratios[i][1]],
            trd_fre_students.iloc[:trd_lang_ratios[i][2]],
        ]).reset_index(drop=True).sort_values(by=['2NDL'])

        df = pd.concat([
            df, partition
        ]).reset_index(drop=True)

        trd_hin_students = trd_hin_students.iloc[trd_lang_ratios[i][0]:]
        trd_nep_students = trd_nep_students.iloc[trd_lang_ratios[i][1]:]
        trd_fre_students = trd_fre_students.iloc[trd_lang_ratios[i][2]:]

    combined_df = pd.concat([df, students_df]).reset_index(drop=True)
    df_groupby = combined_df.groupby(list(combined_df.columns))
    idx = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
    remaining = combined_df.reindex(idx)
    df = pd.concat([df, remaining]).reset_index(drop=True)

    return df

