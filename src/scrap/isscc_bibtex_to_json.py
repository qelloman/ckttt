
import sys
import bibtexparser
import re

def bibtex_entry_to_json_file(entry):
    doi = entry['doi']
    print(doi)
    regex = re.compile(r'^\d+.\d+/(\D+)\.(\d+)\.(\d+)$')
    matchobj = regex.search(doi)
    publication = matchobj.group(1)
    if publication == 'ISSCC':
        publication_type = 1
    elif publication == 'JSSC':
        publication_type = 0
    else:
        publication_type = 99
    year = entry['year'] 
    ieee_id = matchobj.group(3)
    entry_str=''
    entry_str += '   {\n'
    entry_str += '       \"doi": \"'+entry['doi']+'\", \n'
    entry_str += '       \"id": ' + id + ',\n'

    authors_list = entry['author'].split(' and ')
    authors_str = ''
    authors_str += '['
    if len(entry['author']) != 0:
        authors_str += '"{0}"'.format('", "'.join(authors_list))
    authors_str += '],\n'
    entry_str += '       \"author": '
    entry_str += authors_str

    entry_str += '       \"title": \"'+entry['title']+'\", \n'
    entry_str += '       \"publication": \"'+ publication + '\", \n'
    entry_str += '       \"year": '+ year + ',\n'

    keywords_list = entry['keywords'].split(';')
    keywords_str = ''
    keywords_str += '['
    if len(entry['keywords']) != 0:
        keywords_str += '"{0}"'.format('", "'.join(keywords_list))
    keywords_str += '],\n'
    entry_str += '       \"keywords": '
    entry_str += keywords_str 
    entry_str += '       \"abstract": \"'+ entry['abstract'].replace('"', '\\"') + '\"\n'

    entry_str += '  }\n'
    return entry_str
        

def bibtex_to_json(publication):
    with open('./bibtex/'+ publication + '.bibtex') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    with open('./json/' + publication + '.json', 'w') as json_file:
        json_file.write('[\n')
        json_file.write('   ,\n'.join('{0}'.format(bibtex_entry_to_json_file(entry)) for entry in bib_database.entries))
        #for entry in bib_database.entries:
        #    bibtex_entry_to_json_file(entry, json_file)
        json_file.write(']\n')

if __name__ == '__main__':
    bibtex_to_json(sys.argv[1])  

