#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import lucene
from java.io import File
from org.apache.lucene import analysis, document, index, queryparser, search, store, util
from lupyne import engine
import csv
from lupyne.engine import Query

lucene.initVM()

analyzer = analysis.standard.StandardAnalyzer(util.Version.LUCENE_CURRENT)

# Store the index in memory:
# directory = store.RAMDirectory()
# To store an index on disk, use this instead:
# Directory directory = FSDirectory.open(File("/tmp/testindex"))
directory = store.FSDirectory.open(File("./testindex"))
config = index.IndexWriterConfig(util.Version.LUCENE_CURRENT, analyzer)

def create_index():
    iwriter = index.IndexWriter(directory, config)
    with open('data/location.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            province = row['province']
            city = row['city']
            zone = row['zone']
            tone = row['tone']
            lng = row['lng']
            lat = row['lat']
            doc = document.Document()
            doc.add(document.Field("province", province, document.TextField.TYPE_STORED))
            doc.add(document.Field("city", city, document.TextField.TYPE_STORED))
            doc.add(document.Field("zone", zone, document.TextField.TYPE_STORED))
            doc.add(document.Field("tone", tone, document.TextField.TYPE_STORED))
            doc.add(document.Field("lng", lng, document.TextField.TYPE_STORED))
            doc.add(document.Field("lat", lat, document.TextField.TYPE_STORED))
            iwriter.addDocument(doc)
    iwriter.close()

# create_index()

# Now search the index:
def search():
    ireader = index.IndexReader.open(directory)
    isearcher = search.IndexSearcher(ireader)

    parser = queryparser.classic.QueryParser(util.Version.LUCENE_CURRENT, "tone", analyzer)
    query = parser.parse("电子城街道")

    hits = isearcher.search(query, None, 1000).scoreDocs

    ireader.close()
    return hits
directory.close()