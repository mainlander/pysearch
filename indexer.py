import sys, lucene
from os import path, listdir
import glob

from java.nio.file import Paths
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import SimpleFSDirectory, RAMDirectory
from datetime import datetime

from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig

import uuid

INPUT_DIR = 'T/'
INDEX_DIR = 'lucene_index/'

def create_document(file_name):
    path = file_name # assemble the file descriptor
    f = open(path, 'r', encoding='UTF-8') # open in read mode
    doc = Document() # create a new document
    # add the title field
    doc.add(StringField("docid", str(uuid.uuid4()), Field.Store.YES))
    doc.add(StringField("filename", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("text", f.read(), Field.Store.YES))
    f.close() # close the file pointer
    return doc

# Initialize lucene and the JVM
lucene.initVM()

store = SimpleFSDirectory(Paths.get(INDEX_DIR))
analyzer = WhitespaceAnalyzer()
config = IndexWriterConfig(analyzer)
writer = IndexWriter(store, config)

for input_file in glob.iglob(INPUT_DIR + '**/*.txt', recursive=True): # iterate over all input files
    print("Current file:", input_file)
    if input_file.endswith(".txt"): # consider only .txt files
        doc = create_document(input_file) # call the create_document function
        writer.addDocument(doc) # add the document to the IndexWriter

#print("Number of indexed documents: %d\n" % writer.numDocs())
writer.close()
print("Index Done!")

