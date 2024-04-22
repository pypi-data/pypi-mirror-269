from concurrent import futures
from urllib import request

import pathlib
import os


storage = f"{os.getenv('HOME')}/.imdatasets"


class Datasets:
    def __getattr__(self, name):
        if name.startswith("local_"):
            return f"{storage}/{name[6:].replace('_', '.')}.tsv.gz"
        elif name.startswith("remote_"):
            return f"https://datasets.imdbws.com/{name[7:].replace('_', '.')}.tsv.gz"
        else:
            raise AttributeError(name)

    def mapping(self):
        return {
            getattr(self, f"remote_{name}"): getattr(self, f"local_{name}")
            for name in [
                "name_basics",
                "title_basics",
                "title_principals",
                "title_ratings",
            ]
        }

    def download(self):
        pathlib.Path(storage).mkdir(parents=True, exist_ok=True)
        with futures.ThreadPoolExecutor() as executor:
            executor.map(
                lambda rem_loc: request.urlretrieve(rem_loc[0], rem_loc[1]),
                self.mapping().items(),
            )