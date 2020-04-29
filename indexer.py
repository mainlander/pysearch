import sys, lucene
import glob
from datetime import datetime
import uuid

from java.nio.file import Paths
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig


INPUT_DIR = 'T/' #要建立索引的來源檔案目錄
INDEX_DIR = 'lucene_index/' #存放索引的目錄，會自動產生

def create_document(file_path):
    f = open(file_path, 'r', encoding='UTF-8') # 開啟檔案
    doc = Document() # 建立 Lucene document
    # 於 document 中加入一般字串欄位
    # docid 利用 uuid 隨機產生 (單純範例用，實際應用需應需求調整)
    doc.add(StringField("docid", str(uuid.uuid4()), Field.Store.YES))
    doc.add(StringField("filename", input_file, Field.Store.YES))
    # 於 document 中加入文本全文內容
    doc.add(TextField("text", f.read(), Field.Store.YES))
    f.close() # 關檔
    return doc

# 初始化 JAVA 虛擬機器 JVM 與 Lucene (一開始一定要做！)
lucene.initVM()

store = SimpleFSDirectory(Paths.get(INDEX_DIR)) #建立以檔案目錄方式存放的索引
analyzer = WhitespaceAnalyzer() #使用以空白字元作為分隔的內容分析器 (因為分詞結果中間已經以空白隔開了)
config = IndexWriterConfig(analyzer)
writer = IndexWriter(store, config) #建立 IndexWriter 索引寫入器

for input_file in glob.iglob(INPUT_DIR + '**/*.txt', recursive=True): #找出目錄中所有的檔案 
    print("Current file:", input_file)
    if input_file.endswith(".txt"): # 僅考慮 .txt 檔案
        doc = create_document(input_file) # 呼叫先前的 create_document 函式，取得Lucene Document
        writer.addDocument(doc) # 將 document 加到 IndexWriter 裡面

writer.close() #關閉 IndexWriter
print("Index Done!")

