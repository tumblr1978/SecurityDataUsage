## README

This folder provides essential libraries and java source code to query data from dblp database.

---

#### File Description

**folder data**: contains all output produced by the program.

**folder mmdbDoc**: documantion for mmdb package. It is downloaded from http://dblp.org/src/mmdb-2016-12-09-javadoc.jar . The jar file can be extracted by using *jar -xvf ~/Downloads/mmdb-2016-12-09-javadoc.jar* command. 

**confList.txt**: provides a lists of interesting conferences. It collects each conference name and its corresponding dblp abbreviation, separated by comma.

**.xml.zip**: dblp database downloaded from http://dblp.org/xml/release/ ***this file is too large, can't upload to github, need to download manually***

**mmdb-2016-12-09.jar** and **.dtd**: files essential to run the program. Downloaded from http://dblp.org/src/mmdb-2016-12-09.jar and http://dblp.org/xml/release/

**DblpExampleParser copy.java**: example dblp database parser downloaded from http://dblp.org/src/DblpExampleParser.java

**DblpPaperListParser.java**: it queries dblp database with a given conference list file and a given year. It takes three commandline arguments: *dblp_database*,*conference_list*, and *year*. It produces a spreadsheet named as *papersYEAR.csv* stored in *data* folder contains all papers from those conferences in that particular year. Each entry is formatted as: *Paper_title, URL, conferece, year*

---

#### Commands to Run Programs

First of all, unzip the .xml.zip file.

    javac -cp mmdb-2016-12-09.jar Program.java   (*ex. javac -cp mmdb-2016-12-09.jar DblpPaperListParser.java*)
    java -cp mmdb-2016-12-09.jar:. DblpExampleParser Arguments (*ex. java -cp mmdb-2016-12-09.jar:. -DentityExpansionLimit=2000000 DblpPaperListParser dblp-2016-11-02.xml confList.txt 2012*)



