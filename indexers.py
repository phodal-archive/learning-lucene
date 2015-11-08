#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import lucene
from java.io import File
from org.apache.lucene import analysis, document, index, queryparser, search, store, util
from lupyne import engine
import csv
from lupyne.engine import Query

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
        phone = row['联系电话']
        tec = row['QQ/微信']
        email = row['Email']
        office = row['工作单位']
        doc = document.Document()
        doc.add(document.Field("name", name, document.TextField.TYPE_STORED))
        doc.add(document.Field("sex", sex, document.TextField.TYPE_STORED))
        doc.add(document.Field("year", year, document.TextField.TYPE_STORED))
        doc.add(document.Field("phone", phone, document.TextField.TYPE_STORED))
        doc.add(document.Field("tec", tec, document.TextField.TYPE_STORED))
        doc.add(document.Field("email", email, document.TextField.TYPE_STORED))
        doc.add(document.Field("office", office, document.TextField.TYPE_STORED))
        iwriter.addDocument(doc)
iwriter.close()

# Now search the index:
ireader = index.IndexReader.open(directory)
isearcher = search.IndexSearcher(ireader)
# Parse a simple query that searches for "text":
# parser = queryparser.classic.QueryParser(util.Version.LUCENE_CURRENT, "name", analyzer)
# query = parser.parse("赵钱孙李周吴郑王")
# query = search.TermQuery(index.Term('name', "search.TermQuery(index.Term('text', 'lucene'))"))
# query= search.TermQuery(index.Term('sex', '女'))

query = search.PhraseQuery()
query.add(index.Term('name', '赵'))

hits = isearcher.search(query, None, 1000).scoreDocs
# print hits.doc
# Iterate through the results:

for hit in hits:
    hitDoc = isearcher.doc(hit.doc)
    if hitDoc['office'] :
        print hitDoc['name'], hitDoc['sex'], hitDoc['tec'], hitDoc['email']
ireader.close()
directory.close()