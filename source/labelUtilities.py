import csv, json, scopus_data
import utilities

def to_dict(DOI, title, abstract, coverDate, link, label):
    return {
        "DOI": DOI,
        "Title": title,
        "Abstract": abstract,
        "Date": coverDate,
        "Link": link,
        "Label": label
     }

class CategoryHandler:
    def __init__(self):
        pass

    @staticmethod    
    def categoryCount(articles):
        timeSpan = utilities.timeArray()  
        print(articles)
        timeSpan.add_from_articles(articles)
        return timeSpan
    
    @staticmethod   
    def writeCategory(dictionaryArray, file):
        file += ".txt"
        print("printing data to txt file")
        print(dictionaryArray)
        with open(file, 'w', encoding='utf-8') as file:
            for dict in dictionaryArray:
                json.dump(dict, file, ensure_ascii=False, indent=4)
        
            




        