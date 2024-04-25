# OAPapersLoader
This repository contains python loaders for OAPapers corpus and derived datasets. It accompanies the repository [https://github.com/KNOT-FIT-BUT/OAPapers](https://github.com/KNOT-FIT-BUT/OAPapers) and provides more lightweight solution without exhaustive dependencies to load the OAPapers corpus and derived datasets.


## Install

    pip install oapaersloader

## Usage
An example of loading OARelatedWork dataset with references:

```python
from oapapersloader.datasets import OARelatedWork, OADataset

with OARelatedWork("train.jsonl", "train.jsonl.index") as dataset, \
            OADataset("references.jsonl", "references.jsonl.index") as references:
    d = dataset[0]
    print("Document:", dataset[0].title)
    print("Cited paper:", references.get_by_id(d.citations[0]).title)
```
The OARelatedWork will load the target papers with related work sections and the OADataset will load dataset of all references
that can be used for loading cited papers.