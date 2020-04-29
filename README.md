# PyLucene for CBETA 簡單範例

## 1. PyLucene 安裝 (於Ubuntu Linux 18.04 with Anaconda)

### 1.1 安裝相關套件

    sudo apt install openjdk-8-jdk

    sudo apt-get install ant

    sudo apt-get install build-essential

    sudo apt-get install manpages-dev

    sudo apt-get install python3-dev


### 1.2 下載 PyLucene

http://apache.stu.edu.tw/lucene/pylucene/pylucene-8.1.1-src.tar.gz

### 1.3 修改設定檔

    tar -zxvf pylucene-8.1.1-src.tar.gz
    
    cd pylucene-8.1.1/jcc/
    
    vim setup.py
    
修改JDK 設定，把 ‘linux’ 部分改成系統內安裝 Java jdk 的位置

    JDK = {
        'darwin': JAVAHOME or JAVAFRAMEWORKS,
        'ipod': '/usr/include/gcc',
        'linux': '/usr/lib/jvm/java-8-openjdk-amd64',
        'sunos5': '/usr/jdk/instances/jdk1.6.0',
        'win32': JAVAHOME,
        'mingw32': JAVAHOME,
        'freebsd7': '/usr/local/diablo-jdk1.6.0'
    }

執行 jcc 安裝

    /usr/local/anaconda3/bin/python setup.py build
    
    sudo /usr/local/anaconda3/bin/python setup.py install


回到上一層 pylucene 位置後，修改 Makefile

    cd ..
    
    vim Makefile

uncomment 其中一個設定，並修改 JAVA_HOME 為 JDK 安裝位置

    PREFIX_PYTHON=/usr/local/anaconda3
    ANT=JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 /usr/bin/ant
    PYTHON=$(PREFIX_PYTHON)/bin/python3
    JCC=$(PYTHON) -m jcc --shared
    NUM_FILES=10

存擋後，就可以執行編譯與安裝了

### 1.4 執行編譯與安裝

    make
    
    sudo make install

### 1.5 驗證 pylucene 是否安裝成功

進入 test3 資料夾內執行測試程式

    python test_PyLucene.py

若出現 OK 即表示安裝已完成且正確

## 2. pysearch 範例程式

### 2.1 檔案說明
* indexer.py
  * 建立Lucene倒置索引的程式
* searcher.py
  * 以建立出來的Lucene索引進行查詢的程式
* T/
  * 經過分詞的 CBETA 大正藏純文字檔案目錄 (舊版分詞結果)

### 2.2 使用方式

建立索引：

    python index.py

進行查詢：

    python search.py
