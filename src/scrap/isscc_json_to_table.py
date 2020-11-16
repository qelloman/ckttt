import pymysql
import json
import sys
def getConnection(): 
    return pymysql.connect(host='localhost', user='root', password='Dixhtldh119!',
                           db='papers', charset='utf8mb4')

def openJsonfile(filename): 
    with open('./json/' + filename + '_ref.json') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data

def json_to_table_ref(filename): 
    json_data = openJsonfile(filename) 
    conn = getConnection()
    curs = conn.cursor()

    for json_entry in json_data:
        id = json_entry['ieee_id']
        print(id)
        doi = json_entry['doi']
        author = ", ".join(str(x) for x in json_entry['author'])
        title = json_entry['title']
        publication = json_entry['publication']
        if (publication == 'ISSCC'):
            publication_type = 1
        elif (publication == 'JSSC') :
            publication_type = 0
        else:
            publication_type = 99
        year = json_entry['year']
        keywords = ", ".join(str(x) for x in json_entry['keywords'])
        abstract = json_entry['abstract']
        if (author and keywords):
            sql = "insert into paper_info (id,doi,author,title,publication,publication_type,year,keywords,abstract) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
            curs.execute(sql, (str(id), doi, author, title, publication, str(publication_type), str(year), keywords, abstract))
    conn.commit()
    conn.close()

def json_to_table_info(publication): 
    json_data = openJsonfile(publication) 
    conn = getConnection()
    curs = conn.cursor()

    for json_entry in json_data:
        id = json_entry['ieee_id']
        print(id)

        for ref_id in json_entry['references']:
            sql = "insert into paper_ref (id, ref_id) values (%s, %s) "
            curs.execute(sql, (str(id), str(ref_id)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    json_to_table_ref(sys.argv[1])  
    json_to_table_info(sys.argv[1])  

