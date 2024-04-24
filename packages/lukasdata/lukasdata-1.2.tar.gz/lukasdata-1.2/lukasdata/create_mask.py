import pandas as pd


def create_in_mask(mask_series,series_2,in_bool=True):
    mask=[]
    if type(series_2)==pd.Series:
        series_2=series_2.to_list()
    for entry in mask_series:
        if entry in series_2:
            mask.append(in_bool)
        else:
            mask.append(not in_bool)
    return mask
