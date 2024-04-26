import pandas as pd
def filter_numeric_columns(df):
    columns=df.columns
    new_df=pd.DataFrame()
    for column_name in columns:
        column=df[column_name]
        first_value=column[0]
        try:
            pd.to_numeric(df[column_name])
            new_df[column_name]=column
            print(column_name)
        except ValueError:
            print(f"{column_name} can't be converted to numeric")
    return new_df

