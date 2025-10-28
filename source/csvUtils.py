import csv


def has_header(file): 
    header = ['DOI;"Title";"Abstract";"Date";"Link";"CitationCount";"Label"']
    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        for lines in reader:
            return lines == header
        
        return False
    


        



