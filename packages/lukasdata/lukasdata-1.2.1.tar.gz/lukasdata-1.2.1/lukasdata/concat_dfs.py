import pandas as pd

def concat_dfs(dataframes):
    concat_frames=[dataframe.reset_index(drop=True) for dataframe in dataframes]
    df=pd.concat(concat_frames,ignore_index=True)
    return df