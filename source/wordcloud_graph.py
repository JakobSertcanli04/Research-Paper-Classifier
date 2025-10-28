from entryUtilities import CsvFile
from utilities import filterStopWords
from wordcloud import WordCloud, STOPWORDS
import threading
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') 
def run_wordcloud(filepath, log_callback, citation_threshold=15):
    def task():
        try:
            log_callback("Generating Word Cloud...")
            csvFile_instance = CsvFile()
            articles = csvFile_instance.readData(filepath)

            abstracts = " ".join([
                filterStopWords(article["Abstract"])
                for article in articles
                if int(article.get('CitationCount', 0)) >= citation_threshold
            ])

            if not abstracts.strip():
                log_callback("No valid abstracts with sufficient citations.")
                return

            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(
                max_font_size=50,
                max_words=100,
                stopwords=stopwords,
                background_color="white",
                width=800,
                height=600
            ).generate(abstracts)

            # Save the wordcloud
            wordcloud.to_file("wordcloud.png")

            # Display the wordcloud
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout()
            plt.show()

            log_callback("Word Cloud generated and saved as 'wordcloud.png'")
        except Exception as e:
            log_callback(f"Error generating word cloud: {e}")
    threading.Thread(target=task).start()

def run_wordcloud_by_category(filepath, log_callback, citation_threshold=15):
    """Generate word clouds for each category separately"""
    def task():
        try:
            log_callback("Generating Word Clouds by Category...")
            csvFile_instance = CsvFile()
            articles = csvFile_instance.readData(filepath)

            if 'Label' not in articles[0] if articles else {}:
                log_callback("No Label column found. Please run classification first.")
                return

            # Group articles by label
            categories = {}
            for article in articles:
                if int(article.get('CitationCount', 0)) >= citation_threshold:
                    label = article.get('Label', 'Uncategorized')
                    if label not in categories:
                        categories[label] = []
                    categories[label].append(article)

            if not categories:
                log_callback("No articles with sufficient citations found.")
                return

            # Generate word cloud for each category
            for category, category_articles in categories.items():
                abstracts = " ".join([
                    filterStopWords(article["Abstract"])
                    for article in category_articles
                ])

                if abstracts.strip():
                    stopwords = set(STOPWORDS)
                    wordcloud = WordCloud(
                        max_font_size=50,
                        max_words=80,
                        stopwords=stopwords,
                        background_color="white",
                        width=600,
                        height=400
                    ).generate(abstracts)

                 
                    filename = f"wordcloud_{category.replace(' ', '_')}.png"
                    wordcloud.to_file(filename)
                    log_callback(f"Word cloud for '{category}' saved as '{filename}'")

            log_callback("All category word clouds generated successfully.")
        except Exception as e:
            log_callback(f"Error generating category word clouds: {e}")
    threading.Thread(target=task).start()

