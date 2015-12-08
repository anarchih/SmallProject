import pandas as pd

data = pd.read_csv("data.tsv", sep="\t")

data = data.sort(['發病日期'])
data = data.reset_index()
del data['index']
data.to_csv("sorted.tsv", sep="\t", index=False)
