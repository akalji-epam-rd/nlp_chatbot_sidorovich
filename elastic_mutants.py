#!/usr/bin/env python
# coding: utf-8


from elasticsearch import Elasticsearch

es = Elasticsearch()
mutants = open("mutants.txt",'r')
num = 1
for line in mutants:
    list_mut = line.split(':')
    doc = {
        'title': list_mut[0],
        'description': list_mut[1]
    }
    res = es.index(index="desc", doc_type = 'mutants', id = num, body = doc)
    num += 1
mutants.close()