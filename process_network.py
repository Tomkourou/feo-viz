import pandas as pd

from app import get_generation

df = get_generation()

df.to_csv("hourly_generation.csv")
