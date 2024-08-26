import pandas as pd

def second_lang_sort(sections, remainder, students, second_langs, students_df):
    nep_students = students_df.loc[students_df['2NDL'] == second_langs[0]]
    hin_students = students_df.loc[students_df['2NDL'] == second_langs[1]]
    nep_hin_ratio = float("{:.2f}".format(len(nep_students) / len(hin_students)))

    start_index = 0
    hin_nep_ratios = []
    for i in range(sections):
        end_index = start_index + students

        if i < remainder:
            end_index += 1

        total_parts = nep_hin_ratio + 1
        diff = end_index - start_index

        num_nep = round((nep_hin_ratio / total_parts) * diff)
        num_hin = round((1 / total_parts) * diff)

        hin_nep_ratios.append((num_hin, num_nep))

        start_index = end_index

    df = pd.DataFrame()

    for i in range(sections):
        partition = pd.concat([
            hin_students.iloc[:hin_nep_ratios[i][0]],
            nep_students.iloc[:hin_nep_ratios[i][1]]
        ])

        df = pd.concat([df, partition]).reset_index(drop=True)

        hin_students = hin_students.iloc[hin_nep_ratios[i][0]:]
        nep_students = nep_students.iloc[hin_nep_ratios[i][1]:]

    combined_df = pd.concat([df, students_df]).reset_index(drop=True)
    df_groupby = combined_df.groupby(list(combined_df.columns))
    idx = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
    remaining = combined_df.reindex(idx)
    df = pd.concat([df, remaining]).reset_index(drop=True)

    return df

