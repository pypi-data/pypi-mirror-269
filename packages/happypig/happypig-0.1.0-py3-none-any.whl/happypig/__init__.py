import os
from happypig.saying import saying
import pandas as pd

def get_version():
    filename = os.path.join(os.path.dirname(__file__), "VERSION.txt")
    with open(filename) as fr:
        version = fr.read().strip()
    return version

def parse_predefined_animals():
    datapath = os.path.join(os.path.dirname(__file__), "data/animals.csv")
    animals = pd.read_csv(datapath, dtype=str).fillna("").to_dict("records")
    return animals


__version__ = get_version()
animals = parse_predefined_animals()
default_animal = [animal for animal in animals if "happy pig" in animal["animal"]][0]
