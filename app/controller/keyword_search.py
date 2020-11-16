import json
import pymysql

def getConnection():
    conn = pymysql.connect(host='localhost', user='root', password='Dixhtldh119!',
                           db='papers', charset='utf8mb4')
    return conn

def keyword_search(keyword):

    node_sql = \
    "with recursive paper_node (id, title, year, publication, publication_type) as ( " + \
    "select id, title, year, publication, publication_type from paper_info where (title like \'%{0}%\' or keywords like \'%{0}%\') " + \
    "union distinct " + \
    "select info.id, info.title, info.year, info.publication, info.publication_type " + \
    "from " + \
    "(select ref.ref_id as id " + \
    "from " + \
    "paper_ref as ref, paper_node as net " + \
    "where ref.id=net.id " + \
    "group by ref.ref_id) as refresult " + \
    "inner join paper_info as info " + \
    "on info.id = refresult.id) " + \
    "select * from paper_node order by year DESC; "

    link_sql = \
    "with recursive paper_link (source, target) as (" + \
    "select id,  ref_id from " + \
    "(select ref.* from " + \
    "paper_ref as ref, " + \
    "(select id, title, year from paper_info info where (title like \'%{0}%\' or keywords like \'%{0}%\')) as keyword_info " + \
    "where keyword_info.id = ref.id) as result " + \
    "where exists (select * from paper_info where result.ref_id = paper_info.id) " + \
    "union distinct " + \
    "select * from " + \
    "(select ref.* " + \
    "from " + \
    "paper_ref as ref, paper_link as link " + \
    "where ref.id=link.target " + \
    ") as result " + \
    "where exists (select * from paper_info where result.ref_id = paper_info.id) " + \
    ") " + \
    "select * from paper_link;"
    conn = getConnection()
    curs = conn.cursor()

    data = {}
   
    curs.execute(node_sql.format(keyword))
    data['nodes'] = [{"id":a, "title":b, "year":c, "publication":d, "publication_type":e} for a,b,c,d,e in curs.fetchall()]
    
    curs.execute(link_sql.format(keyword))
    data['links'] = [{"from":a, "to":b} for a,b in curs.fetchall()]
    conn.close()
    
    return json.dumps(data, indent=4)
