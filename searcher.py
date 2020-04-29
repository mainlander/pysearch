import sys, lucene
from os import path, listdir
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory, RAMDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

INDEX_DIR = 'lucene_index/'

MAX_COUNT = 100

def search_loop(searcher, analyzer):
    while True:
        print("\nEnter a blank line to quit.")
        command = input("Query: ")
        if command == '':
            return

        print("Searching for:", command)
        query = QueryParser("text", analyzer).parse(command)
        start = datetime.now()
        scoreDocs = searcher.search(query, MAX_COUNT).scoreDocs
        duration = datetime.now() - start
        print("%s total matching documents in %s:" % (len(scoreDocs), duration))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print(doc.get("docid"), doc.get('filename'), scoreDoc.score)#, 'name:', doc.get("name")

        print("\n------------------------------------------------------")

# Initialize lucene and the JVM
lucene.initVM()

store = SimpleFSDirectory(Paths.get(INDEX_DIR))
searcher = IndexSearcher(DirectoryReader.open(store))
analyzer = WhitespaceAnalyzer()

search_loop(searcher, analyzer)
