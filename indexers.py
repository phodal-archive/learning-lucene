#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import lucene
from java.io import File
from org.apache.lucene import analysis, document, index, queryparser, search, store, util
from lupyne import engine
import csv

lucene.initVM()

# # # lucene # # #

analyzer = analysis.standard.StandardAnalyzer(util.Version.LUCENE_CURRENT)

# Store the index in memory:
# directory = store.RAMDirectory()
# To store an index on disk, use this instead:
# Directory directory = FSDirectory.open(File("/tmp/testindex"))
directory = store.FSDirectory.open(File("./testindex"))
config = index.IndexWriterConfig(util.Version.LUCENE_CURRENT, analyzer)
iwriter = index.IndexWriter(directory, config)
with open('data/xiaoyou.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['姓名']
        sex = row['性别']
        year = row['毕业年份']
        doc = document.Document()
        doc.add(document.Field("name", name, document.TextField.TYPE_STORED))
        doc.add(document.Field("sex", sex, document.TextField.TYPE_STORED))
        doc.add(document.Field("year", year, document.TextField.TYPE_STORED))
        iwriter.addDocument(doc)
iwriter.close()

# Now search the index:
ireader = index.IndexReader.open(directory)
isearcher = search.IndexSearcher(ireader)
# Parse a simple query that searches for "text":
parser = queryparser.classic.QueryParser(util.Version.LUCENE_CURRENT, "name", analyzer)
query = parser.parse("张")
hits = isearcher.search(query, None, 1000).scoreDocs
print len(hits)
# Iterate through the results:
# for hit in hits:
#     hitDoc = isearcher.doc(hit.doc)
#     assert hitDoc['fieldname'] == text
ireader.close()
directory.close()