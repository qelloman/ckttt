import re

# Initialize with bibtex
class Paper():
    def __init__(self, bibtex_entry):
        self.doi = bibtex_entry['doi']
        self.year = bibtex_entry['year'] 
        self.title = bibtex_entry['title']
        self.id = bibtex_entry['ID']
        regex = re.compile(r'^\d+.\d+/(\D+)\.(\d+)\.(\d+)$')
        matchobj = regex.search(self.doi)
        self.publication = matchobj.group(1)
        if self.publication == 'ISSCC':
            self.publication_type = 1
        elif self.publication == 'JSSC':
            self.publication_type = 0
        else:
            self.publication_type = 99

        self.authors = bibtex_entry['author'].split(' and ')
        self.keywords = bibtex_entry['keywords'].split(';')
        self.abstract = bibtex_entry['abstract']

    def getId(self):
        return self.id

    def getDoi(self):
        return self.doi

    def getTitle(self):
        return self.title

    def getYear(self):
        return self.year

    def getPublication(self):
        return self.publication

    def getPublication_type(self):
        return self.publication_type

    def getAuthors(self):
        return self.authors

    def getKeywords(self):
        return self.keywords
    
    def setRefs(self, refs):
        self.refs = refs 
    
    def getRefs(self):
        return self.refs 

    def getKeywords_str(self):
        keywords_str = ''
        if len(self.keywords) > 0:
            keywords_str += '"{0}"'.format('", "'.join(self.keywords))
        return keywords_str 
    
    def getAuthors_str(self):
        authors_str = ''
        if len(self.authors) > 0:
            authors_str += '"{0}"'.format('", "'.join(self.authors))
        return authors_str 

    def getAbstract(self):
        return self.abstract

    def isPaper(self):
        return (len(self.authors) > 0 and len(self.keywords) > 0)

