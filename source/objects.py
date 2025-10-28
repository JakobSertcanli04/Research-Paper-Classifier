
class Journal:
    def __init__(self, isnn, title, articleList, articleListCount):
        self.title = title
        self.isnn = isnn
        self.articles = articleList
        self.articleListCount = articleListCount      

    def to_dict(self, csvFileArticles):
        return {
            "title": self.title,
            "isnn": self.isnn,
            "articleListCount": self.articleListCount,
            "csvFileArticles": csvFileArticles
        }
    
class Article:
    def __init__(self, DOI, title, abstract, coverDate, citationCount, link):

        self.DOI = DOI
        self.Title = title
        self.Abstract = abstract
        self.CoverDate = coverDate
        self.Link = link
        self.CitationCount = citationCount
        self.Label = "None"

    def __str__(self):
        return f"doi: {self.DOI}, title: {self.Title}, abstract: {self.Abstract}, date: {self.CoverDate}"

    def __eq__(self, other):
        return isinstance(other, Article) and self.DOI == other.DOI

    def __hash__(self):
        return hash((self.DOI))

    def to_dict(self):
        return {
            "DOI": self.DOI,
            "Title": self.Title,
            "Abstract": self.Abstract,
            "Date": self.CoverDate,
            "Link": self.Link,
            "Label": self.Label,
            "CitationCount": self.CitationCount
        }
class getData:
    def __init__(self, ArticleData):
        if isinstance(ArticleData, Article):

            self.__title = Article.Title
            self.__doi = Article.DOI
            self.__coverDate = Article.CoverDate
            self.__abstract = Article.Abstract

        else:
            raise TypeError("Expected an object of the type Article!")

    
    