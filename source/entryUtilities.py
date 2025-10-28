
import re
from objects import Article, Journal
import csv
from csvUtils import has_header

def getAbstractData(file):
    data = []
    with open(file) as file_obj:
        
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)                        
        for row in reader_obj:
            cleanedAbstract = re.sub(r'\W+', '', row["Text"])
            data.append({'Label': row["Label"], 'Text': cleanedAbstract})
        
    return data



class CsvFile:

    def __init__(self):
        pass

    def readData(self, fileName):
        with open(fileName, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=";")         
            return list(reader)

    def writeDataJournal(self, journal, csvFileArticles, csvFileJournal):
        if isinstance(journal, Journal):
            journalDict = Journal.to_dict(journal, csvFileArticles)
            fieldnames = ['isnn', 'title', 'articleListCount', 'csvFileArticles']

            with open(csvFileJournal, mode='w', newline='', encoding='utf-8') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, delimiter=';')
                writer.writerow(journalDict)

        
    def writeDataArticles(self, csvFileArticles, articleList):
            fieldnames = ['DOI', 'Title', 'Abstract', 'Date', 'Link', 'CitationCount', 'Label']
            with open(csvFileArticles, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, delimiter=';')

                if has_header(csvFileArticles) == False:
                    writer.writeheader()

                if isinstance(articleList, list):
                    for article in articleList:
                        writer.writerow(Article.to_dict(article))
                else:
                    raise ValueError("Data must be a list.") 
        
    def writeLabeledDataArticles(self, csvFileArticles, articleList):
            fieldnames = ['DOI', 'Title', 'Abstract', 'Date', 'Link', 'CitationCount', 'Label']



            with open(csvFileArticles, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, delimiter=';')

                if has_header(csvFileArticles) == False:
                    writer.writeheader()

                if isinstance(articleList, list):
                    for article in articleList:
                        if article['Label'] != "Undefined": 
                            writer.writerow(article)
                else:   
                    raise ValueError("Data must be a list.") 
