import sys, lucene
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.core import WhitespaceAnalyzer

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

INDEX_DIR = 'lucene_index/' #建立出來的索引檔的目錄

MAX_COUNT = 100 #搜尋結果最多可以回傳幾筆

def search_loop(searcher, analyzer):
    while True:
        print("\nEnter a blank line to quit.")
        command = input("Query: ")
        if command == '':
            return

        print("Searching for:", command)
        query = QueryParser("text", analyzer).parse(command) #利用 QueryParser 剖析查詢語句，支援 Lucene 查詢語法，請參閱 Lucene 文件。目前針對 Document 的 text 欄位進行查詢
        start = datetime.now()
        scoreDocs = searcher.search(query, MAX_COUNT).scoreDocs #進行搜尋，並取得搜尋結果document
        duration = datetime.now() - start
        print("%s total matching documents in %s:" % (len(scoreDocs), duration))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print(doc.get("docid"), doc.get('filename'), scoreDoc.score) #印出搜搜尋結果欄位以及相關度分數

        print("\n------------------------------------------------------")

# 初始化 Java 虛擬機器 JVM 與 Lucene
lucene.initVM()

store = SimpleFSDirectory(Paths.get(INDEX_DIR)) #讀取索引檔的目錄
searcher = IndexSearcher(DirectoryReader.open(store)) #建立 IndexSearcher 搜尋器
analyzer = WhitespaceAnalyzer() #使用空白字元分析器

search_loop(searcher, analyzer) #開始搜尋
