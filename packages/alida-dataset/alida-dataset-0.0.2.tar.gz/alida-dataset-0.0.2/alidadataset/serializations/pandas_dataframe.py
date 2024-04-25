from pandas import DataFrame
from pandas import read_csv
import pandas as pd
from ..utils import input_or_output, get_asset_property
from dsioutilities import Dataset


def load_dataframe_from_minio(name):
    input_dataset = Dataset(name, dataset_type="tabular")
    if isinstance(input_dataset.get_path(), list):
        df = pd.concat([pd.read_csv(filename) for filename in input_dataset.get_path()])
    else:
        df = pd.read_csv(input_dataset.get_path())
    return df


def load(name)-> DataFrame:
    storage_type = get_asset_property(asset_name=name, property="storage_type")
    if storage_type == "minio":
        return load_dataframe_from_minio(name)
    elif storage_type =="filesystem":
        return read_csv( get_asset_property(asset_name=name))


