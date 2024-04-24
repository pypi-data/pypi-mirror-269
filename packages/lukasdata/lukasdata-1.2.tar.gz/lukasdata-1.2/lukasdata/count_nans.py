def count_nan(df):
    nan_df=df.isna()
    nan_dict={}
    df_len=len(df)
    for column in nan_df.columns:
        nan_dict[column]=nan_df[column].sum()
    nan_dict=dict(sorted(nan_dict.items(), key= lambda x: x[1]))
    print(f"Max len: {df_len}")
    print(nan_dict)
    return nan_dict
    
#nan_counts=count_nan(complete_financial)
