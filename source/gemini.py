"""
Gemini AI classification module for scientific articles.
"""

from google import genai
from entryUtilities import CsvFile
import time


def geminiClassify(input_csv_path, topics, citationCountLimit=10):
    """
    Classify articles using Google's Gemini AI.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        topics (list): List of topics for classification
        citationCountLimit (int): Minimum citation count threshold
        
    Returns:
        list: List of classified articles
    """
    csvFile_instance = CsvFile()
    articles = csvFile_instance.readData(input_csv_path) 
    articleList = []
    
    try:
        citationCountLimit = int(citationCountLimit)
    except (ValueError, TypeError):
        citationCountLimit = 10  # Default value if conversion fails
    
    print(f"Total articles loaded: {len(articles)}")
    print(f"Citation limit: {citationCountLimit}")
    print(f"Topics: {topics}")
    
    # Initialize Gemini client
    client = genai.Client(api_key="")

    articles_processed = 0
    articles_skipped = 0
    
    for i, article in enumerate(articles):
        try:
            
            citation_count = 0
            citation_count_raw = article.get("CitationCount", "0")
            
            if citation_count_raw is not None:

                citation_count_str = str(citation_count_raw).strip()
                
              
                if citation_count_str.isdigit():
                    citation_count = int(citation_count_str)
                else:
                    
                    import re
                    digits = re.findall(r'\d+', citation_count_str)
                    if digits:
                        citation_count = int(digits[0])
                    else:
                        citation_count = 0
            
            print(f"Article {i + 1}: Citation count = {citation_count} (original: '{citation_count_raw}')")
            
            if citation_count >= citationCountLimit:
                articles_processed += 1
                print(f"Processing article {i + 1}/{len(articles)} (citation count: {citation_count})")
                
                
                topics_text = ", ".join(topics)
                prompt = f"""You are a scientific article classifier. Your task is to categorize the following abstract into exactly one of these predefined categories: {topics_text}

CRITICAL RULES:
1. You must choose ONLY ONE category from the list above
2. You must return ONLY the exact category name as written in the list
3. Do not modify, change, or add any words to the category names
4. If the abstract doesn't fit any of the categories, return "Undefined"
5. Do not add numbers, prefixes, or any other text
6. Do not add punctuation marks like periods or commas
7. Pay special attention to exact spelling and capitalization

Available categories: {topics_text}

Abstract to classify: {article['Abstract']}

Return only the category name:"""
                
               
                response = client.models.generate_content(
                    model="gemma-3-27b-it",
                    contents=prompt
                )
                
                classification = response.text.strip()
                print(f"Classification: {classification}")
                
                
                classification = classification.strip()
                classification = classification.rstrip('.,!?')
                
                
                if classification in topics:
                    article['Label'] = classification
                    print(f"✓ Valid classification: {classification}")
                else:
                    article['Label'] = "Undefined"
                    print(f"✗ Invalid classification: '{classification}' not in topics list")
                
                articleList.append(article)
                
               
                time.sleep(2.1)
            else:
                articles_skipped += 1
                print(f"Skipping article {i + 1} (citation count {citation_count} < limit {citationCountLimit})")
                
        except Exception as e:
            print(f"Error processing article {i + 1}: {e}")
            print(f"Article data: {article}")
            
            continue
    
    print(f"\nSummary:")
    print(f"Total articles: {len(articles)}")
    print(f"Articles processed: {articles_processed}")
    print(f"Articles skipped (low citations): {articles_skipped}")
    print(f"Articles with errors: {len(articles) - articles_processed - articles_skipped}")
    
    
    articleList.sort(key=lambda x: x.get('Label', ''))
    
   
    csvFile_instance.writeLabeledDataArticles(input_csv_path, articleList)
    
    return articleList


