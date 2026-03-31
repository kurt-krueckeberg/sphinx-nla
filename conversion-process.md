# Conversion Route

.adoc
  ↓
Asciidoctor → DocBook 5
  ↓
XSLT (db5to4-core.xsl)
  ↓
DocBook 4
  ↓
Pandoc
  ↓
Markdown/MyST


## Setting up the XSLT Piece

1. git clone https://github.com/tomschr/dbcookbook.git && cd dbcookbook

2. cp dbcookbook/en/xml/structure/common/copy.xsl \                                                                                              sphinx-nla
   dbcookbook/en/xml/structure/db5-to-db4/
 
## The First Two Steps

1. Convert .adoc to DocBook 5:

asciidoctor ~/nla/m/1291/p/contents-list.adoc  -b docbook -o ~/temp/doc5.xml

2. Strip the DocBook 5 Namespace

sed 's/xmlns="http:\/\/docbook.org\/ns\/docbook"//' ~/temp/doc5.xml > ~/temp/doc5-nons.xml

3. Change into the stylesheet directory

4. Run the Transformation

xsltproc db5to4.xsl ~/temp/doc5-nons.xml > ~/temp/doc4.xml
