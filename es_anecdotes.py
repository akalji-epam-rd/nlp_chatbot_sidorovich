#!/usr/bin/env python
# coding: utf-8

import json
from elasticsearch import Elasticsearch

es = Elasticsearch()

with open("anecdotes.json", "r") as read_file:
    data = json.load(read_file)

num = 1
for anecdote in data:
    doc = {
        "anecdote": data[anecdote]
    }
    res = es.index(index="jokes", doc_type = 'anecdote', id = num, body = doc)
    num += 1
