import pymysql
import json
import sys
def getConnection(): 
    return pymysql.connect(host='localhost', user='root', password='xhtldh119',
                           db='papers', charset='utf8mb4')

def openJsonfile(filename): 
    with open('./json/' + filename + '_refonly.json') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data

def json_to_table_ref(publication): 
    json_data = openJsonfile(publication) 
    conn = getConnection()
    curs = conn.cursor()

    for json_entry in json_data:
        id = json_entry['id']
        ref_id = json_entry['ref_id']

        sql = "insert into paper_ref (id, ref_id) values (%s, %s) "
        curs.execute(sql, (str(id), str(ref_id)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    json_to_table_ref(sys.argv[1])  

