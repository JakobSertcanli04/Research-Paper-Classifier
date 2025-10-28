import requests
import numpy as np
import csv
from datetime import datetime
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import re
import time
from entryUtilities import CsvFile
from objects import Article, Journal
    
class ScopusData:
    def __init__(self):

        self.apiKey = "0841ac3993f300b244d56e374255bee5"
        self.articleList = []

    def getArticle(self, doi, citationCount):
        url = f"https://api.elsevier.com/content/article/doi/{doi}?apiKey={self.apiKey}&httpAccept=application%2Fjson"
        response = requests.get(url)


        if response.status_code == 200:

            data = response.json()
            exists = str(data.get("search-results", {}).get("opensearch:totalResults", False))

            if exists:             
                abstract = str(data.get("full-text-retrieval-response", {}).get("coredata", {}).get("dc:description", None))
                title = str(data.get("full-text-retrieval-response", {}).get("coredata", {}).get("dc:title", None))
                coverDate = str(data.get("full-text-retrieval-response", {}).get("coredata", {}).get("prism:coverDate", None))
                doi = str(data.get("full-text-retrieval-response", {}).get("coredata", {}).get("prism:doi", None))
                link_list = data.get("full-text-retrieval-response", {}).get("coredata", {}).get("link", None)

                link = str(link_list[1].get("@href", None))
    
                if abstract == "null" or abstract is None or abstract == "None" or title == "null" or title is None or coverDate == "null" or coverDate is None:
                    return None  
                


                abstract = re.sub(r'\s{2,}', ' ', abstract)
                title  = re.sub(r'\s{2,}', ' ', title)
                Article_instance = Article(doi, title, abstract, coverDate, citationCount, link)
                return Article_instance
            
     
        return None    
        
    def getTitle(self, id):

        
        if id is not None:
            url = f"https://api.elsevier.com/content/serial/title/issn/{id}?apiKey={self.apiKey}&httpAccept=application%2Fjson"
        else:
            return False

        response = requests.get(url)
        data = response.json()

       
        if response.status_code == 200:
            entries = data.get("serial-metadata-response", {}).get("entry", [])
            if entries:
                return entries[0].get("dc:title", False)
            else:
               return False     
        else:
            print(f"Error: {response.status_code}")
            response.raise_for_status()
            return False        

    def getJournal(self, id, years, citationLimit):

        ArticleList = []
        nrOfArticles = 0
        title = self.getTitle(id)        
        
        seen_dois = set()   


        if title:  
            for year in years:    

                startIndex = 0
                url = f"https://api.elsevier.com/content/search/scopus?query=ISSN({id})&date={year}&apiKey={self.apiKey}"

                response = requests.get(url)
                data = response.json()

                
                if response.status_code == 200:
                    abstractCount = (data.get("search-results", {}).get("opensearch:totalResults", None))
                    
                    print(abstractCount)

                    if abstractCount is None:
                        continue

                    nrOfArticles += int(abstractCount)   

 
                    for _ in range(int(abstractCount)):

                        url = f"https://api.elsevier.com/content/search/scopus?query=ISSN({id})&start={startIndex}&date={year}&apiKey={self.apiKey}"
                        response = requests.get(url)
                        data = response.json()

                        if response.status_code != 200:
                            break

                        page = (data.get("search-results", {}).get("entry", None))

                        if page is None:
                            break

                        pagesCount = len(page)

                        if pagesCount == 0:
                            break

                        start = time.time()        
                        for i in range(pagesCount):            
                            print(i + startIndex)
                            articleDOI = page[i].get("prism:doi", None)
                            articleCitationCount = page[i].get("citedby-count", None)
                            if articleDOI is not None and int(articleCitationCount) >= citationLimit: 
                                article = self.getArticle(articleDOI, articleCitationCount)
                                
                                if article is not None and article.DOI not in seen_dois:
                                    seen_dois.add(article.DOI)
                                    print(article)
                                    ArticleList.append(article)

                      


                        startIndex += pagesCount + 1

                else:
                    print(f"Error: {response.status_code}")
                    print(year)
                    response.raise_for_status()
                    return None
            time.sleep(300)    
        else:
            print("Please insert a journal")
            return None
            
        print(nrOfArticles)
        return Journal(id, title, ArticleList, nrOfArticles)

        

#ScopusData_instance = ScopusData()
#journal = ScopusData_instance.getJournal("1879-0690", "Sustainable Materials and Technologies")



def yearsArray(firstYear, secondYear):
    years = []
    years.append(firstYear)
    while(firstYear < secondYear):
        years.append(str(firstYear + 1))
        firstYear+=1

    return years










