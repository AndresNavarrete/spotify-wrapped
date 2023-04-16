import pandas as pd


class Dataset:
    def __init__(self):
        self.dataframe = None
        self.items = list()
        self.records = list()

    def set_records(self):
        for item in self.items:
            new_record = vars(item)
            self.records.append(new_record)

    def set_dataframe(self):
        self.dataframe = pd.DataFrame.from_records(self.records)

    def get_dataset(self):
        self.set_records()
        self.set_dataframe()
        return self.dataframe


class TracksDataset(Dataset):
    def __init__(self, tracks):
        super().__init__()
        self.items = tracks


class ArtistDataset(Dataset):
    def __init__(self, artists):
        super().__init__()
        self.items = artists
