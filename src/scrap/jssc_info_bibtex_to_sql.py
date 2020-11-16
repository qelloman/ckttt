import pymysql
import sys 
import bibtexparser
from paper import Paper
def getConnection(): 
    return pymysql.connect(host='localhost', user='root', password='xhtldh119',
                           db='papers', charset='utf8mb4')

def bibtex_entry_to_table(bibtex_entry):
    myPaper = Paper(bibtex_entry)
    if (myPaper.isPaper()):
        #conn = getConnection()
        #curs = conn.cursor()
        sql = "insert into paper_info (id,doi,author,title,publication,publication_type,year,keywords,abstract) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        try:
            #curs.execute(sql, (str(myPaper.getId()),
            print(sql % (str(myPaper.getId()),
                               myPaper.getDoi(),
                               myPaper.getAuthors_str(),
                               myPaper.getTitle(),
                               myPaper.getPublication(),
                               str(myPaper.getPublication_type()),
                               str(myPaper.getYear()),
                               myPaper.getKeywords_str,
                               myPaper.getAbstract()))
        except pymysql.err.IntegrityError:
            print ('Integrity Error')
            pass
        #conn.commit()
        #conn.close()
   
    return
        

def bibtex_to_json(publication):
    with open('./bibtex/'+ publication + '.bibtex') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for bibtex_entry in bib_database.entries:
        bibtex_entry_to_table(bibtex_entry)

if __name__ == '__main__':
    bibtex_to_json(sys.argv[1])  

