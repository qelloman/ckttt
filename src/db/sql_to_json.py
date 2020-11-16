import pymysql
import json

def keyword_search(keyword):

    node_sql = \
    "with recursive paper_node (id, title, year, lv) as ( " + \
    "select ieee_id, title, year, 0 as lv from paper_info where (title like \'%{0}%\' or keywords like \'%{0}%\') and year=2017 " + \
    "union distinct " + \
    "select info.ieee_id, info.title, info.year, refresult.lv " + \
    "from " + \
    "(select ref.ref_id as ieee_id, sum(net.lv + 1) as lv " + \
    "from " + \
    "paper_ref as ref, paper_node as net " + \
    "where ref.ieee_id=net.id " + \
    "group by ref.ref_id) as refresult " + \
    "inner join paper_info as info " + \
    "on info.ieee_id = refresult.ieee_id) " + \
    "select * from paper_node; "

    edge_sql = \
    "with recursive paper_edge (source, target) as (" + \
    "select ieee_id,  ref_id from " + \
    "(select ref.* from " + \
    "paper_ref as ref, " + \
    "(select ieee_id, title, year from paper_info info where (title like \'%{0}%\' or keywords like \'%{0}%\')) as keyword_info " + \
    "where keyword_info.ieee_id = ref.ieee_id) as result " + \
    "where exists (select * from paper_info where result.ref_id = paper_info.ieee_id) " + \
    "union distinct " + \
    "select * from " + \
    "(select ref.* " + \
    "from " + \
    "paper_ref as ref, paper_edge as edge " + \
    "where ref.ieee_id=edge.target " + \
    ") as result " + \
    "where exists (select * from paper_info where result.ref_id = paper_info.ieee_id) " + \
    ") " + \
    "select * from paper_edge;"

    conn = pymysql.connect(host='localhost', user='root', password='Dixhtldh119!',
                           db='papers', charset='utf8mb4')
    curs = conn.cursor()

    data = {}
   
    curs.execute(node_sql.format(keyword))
    data['nodes'] = [{"id":a, "title":b, "year":c, "lv":d} for a,b,c,d in curs.fetchall()]
    
    curs.execute(edge_sql.format(keyword))
    data['edges'] = [{"from":a, "to":b} for a,b in curs.fetchall()]
    conn.close()
    
    return json.dumps(data, indent=4)



if __name__ == '__main__':
    keyword = input("enter keyword to find: ") 
    print (keyword)
    data = keyword_search(keyword)

    with open('../../rsc/json/data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        json_file.close()

