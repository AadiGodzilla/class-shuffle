import pandas as pd

def house_sort(sections, remainder, students, total_students, houses, students_df):
    house_a = students_df.loc[students_df['H'] == houses[0]].reset_index(drop=True)
    house_d = students_df.loc[students_df['H'] == houses[1]].reset_index(drop=True)
    house_g = students_df.loc[students_df['H'] == houses[2]].reset_index(drop=True)
    house_k = students_df.loc[students_df['H'] == houses[3]].reset_index(drop=True)

    house_ratios = []

    start_index = 0
    for i in range(sections):
        end_index = start_index + students
        if i < remainder:
            end_index += 1

        diff = end_index - start_index

        house_a_num = round((len(house_a) / total_students) * diff)
        house_d_num = round((len(house_d) / total_students) * diff)
        house_g_num = round((len(house_g) / total_students) * diff)
        house_k_num = round((len(house_k) / total_students) * diff)

        house_ratios.append((house_a_num, house_d_num, house_g_num, house_k_num))

        start_index = end_index

    df = pd.DataFrame()
    for i in range(sections):
        partition = pd.DataFrame()
        partition = pd.concat([
            house_a.iloc[:house_ratios[i][0]],
            house_d.iloc[:house_ratios[i][1]],
            house_g.iloc[:house_ratios[i][2]],
            house_k.iloc[:house_ratios[i][3]],
        ])

        df = pd.concat([df, partition]).sort_values(by=['2NDL']).reset_index(drop=True)

        house_a = house_a.iloc[house_ratios[i][0]:]
        house_d = house_d.iloc[house_ratios[i][1]:]
        house_g = house_g.iloc[house_ratios[i][2]:]
        house_k = house_k.iloc[house_ratios[i][3]:]

    combined_df = pd.concat([df, students_df]).reset_index(drop=True)
    df_groupby = combined_df.groupby(list(combined_df.columns))
    idx = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
    remaining = combined_df.reindex(idx)
    df = pd.concat([df, remaining]).reset_index(drop=True)

    return df
