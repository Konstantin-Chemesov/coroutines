import pandas as pd


class FileReader:

    def __init__(self) -> None:
        self.json_to_df = pd.DataFrame()

    def read_json(self, path: str) -> None:
        self.json_to_df = pd.read_json(path)

    def json_to_parquet(self, path: str) -> None:
        self.json_to_df.to_parquet(path.replace('json', 'parquet'))

    def start(self, path: str) -> None:
        self.read_json(path)
        self.json_to_parquet(path)
