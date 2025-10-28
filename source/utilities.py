import re
from datetime import datetime

import spacy
nlp = spacy.load("en_core_web_sm")


def filterStopWords(abstract):
    abstract = re.sub(r'-', ' ', abstract)
    filtered = re.sub(r"[.,]", '', abstract)
    doc = nlp(filtered)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return ' '.join(filtered_words)


def doiLink(DOI):
    return DOI.startswith("https://doi.org/")


def removeLink(DOI):
    return re.sub("https://doi.org/", "", DOI)


def getYear(articleDate):
 
    return int(articleDate[:4])


def yearsArray(firstYear, secondYear):
    years = []
    years.append(firstYear)
    while(firstYear < secondYear):
        years.append(str(firstYear + 1))
        firstYear+=1

    return years

class timeArray:
    def __init__(self, start_year=2010, end_year=2025):
        self.years = yearsArray(start_year, end_year)  
        self.YEARS = len(self.years)

     
        self.timeSpanList = []
        for _ in range(self.YEARS):
            self.timeSpanList.append({
                "Total": 0,
                "Uncertain": 0
            })

    def add_from_articles(self, articles):
        print(self.years)
        for article in articles:
            try:
                print("her")
                print(article)
                

                year = getYear(article["Date"])
                year_str = str(year)

                if year_str in self.years:
                    index = self.years.index(year_str)
                    label = article["Label"]

                
                    if label not in self.timeSpanList[index]:
                        self.timeSpanList[index][label] = 0

                    self.timeSpanList[index][label] += 1
                    self.timeSpanList[index]["Total"] += 1
                else:
                    print(f"Year {year} not in range")

            except Exception as e:
                print(f"Error processing article: {e}")


    def __iter__(self):
        return iter(self.timeSpanList)

    def toJson(self):
        import json
        return json.dumps(self.timeSpanList, indent=4)



