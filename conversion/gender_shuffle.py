import pandas as pd

def gender_sort(sections, remainder, students, genders, student_df):
    males = student_df.loc[student_df['G'] == genders[0]]
    females = student_df.loc[student_df['G'] == genders[1]]
    males_female_ratio = float("{:.2f}".format(len(males) / len(females)))

    males_females_ratio_list = []

    start_index = 0
    for i in range(sections):
        end_index = start_index + students

        if i < remainder:
            end_index += 1

        total_parts = males_female_ratio + 1

        diff = end_index - start_index

        num_males = round((males_female_ratio / total_parts) * diff)
        num_females = round((1 / total_parts) * diff)

        males_females_ratio_list.append((num_males, num_females))
        start_index = end_index

    df = pd.DataFrame()

    for i in range(sections):
        partition = pd.concat([
            males.iloc[:males_females_ratio_list[i][0]],
            females.iloc[:males_females_ratio_list[i][1]
            ]])

        df = pd.concat([df, partition]).reset_index(drop=True)

        males = males.iloc[males_females_ratio_list[i][0]:]
        females = females.iloc[males_females_ratio_list[i][1]:]

    combined_df = pd.concat([df, student_df]).reset_index(drop=True)
    df_groupby = combined_df.groupby(list(combined_df.columns))
    idx = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
    remaining = combined_df.reindex(idx)
    df = pd.concat([df, remaining]).reset_index(drop=True)

    return df
