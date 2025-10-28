"""
Article Classification Tool - Gemini Edition
Main application file for classifying scientific articles using Google's Gemini AI.
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import threading
import webbrowser
from labelUtilities import CategoryHandler
from entryUtilities import CsvFile
import scopus_data
from gemini import geminiClassify
from wordcloud_graph import run_wordcloud
import pandas as pd
import plotly.express as px


class ArticleClassifierApp:
    """Main application class for the Article Classification Tool."""
    
    def __init__(self):
        self.window = tk.Tk()
        self.setup_window()
        self.create_ui()
        
    def setup_window(self):
        """Configure the main window."""
        self.window.title("Article Classification Tool")
        self.window.geometry("900x800")
        
    
        style = ttk.Style()
        style.theme_use('clam')
        
    def log(self, msg):
        """Add message to log box."""
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        
    def fetch_articles(self, issn, start_year, end_year, output_path, citation_limit=0):
        """Fetch articles from Scopus."""
        try:
            self.log(f"Fetching articles for ISSN {issn} from {start_year} to {end_year}...")
            scopus_instance = scopus_data.ScopusData()
            years = scopus_data.yearsArray(int(start_year), int(end_year))
            citation_limit = int(citation_limit) if citation_limit else 0

            journal = scopus_instance.getJournal(issn, years, citation_limit)
            csv_instance = CsvFile()
            csv_instance.writeDataArticles(output_path, journal.articles)

            self.log(f"{len(journal.articles)} articles written to: {output_path}")
        except Exception as e:
            self.log(f"Error fetching articles: {e}")
            
    def run_gemini_classification(self, filepath, topics, citation_threshold):
        """Run Gemini classification on articles with enhanced topic processing."""
        try:
       
            if not topics or not topics.strip():
                self.log("Error: No topics provided.")
                return
                
            topics_list = [topic.strip() for topic in topics.split(",")]
            
            # Remove any empty topics and validate
            topics_list = [topic for topic in topics_list if topic and len(topic) > 0]
            
            if not topics_list:
                self.log("Error: No valid topics provided after processing.")
                return
                
            self.log(f"Processing {len(topics_list)} topics: {', '.join(topics_list)}")
            self.log("Running Gemini classification with enhanced prompt structure...")

            articles = geminiClassify(filepath, topics_list, citation_threshold)
            
            if articles:
                categoryCountDict = CategoryHandler.categoryCount(articles)
                CategoryHandler.writeCategory(categoryCountDict, filepath)
                self.log(f"Classification complete. Processed {len(articles)} articles.")
                
                if categoryCountDict:
                    self.log("Classification summary:")
                    for category, count in categoryCountDict.items():
                        self.log(f"  {category}: {count} articles")
                else:
                    self.log("No articles were classified into the provided categories.")
            else:
                self.log("No articles were processed during classification.")
                
        except Exception as e:
            self.log(f"Error in classification: {e}")
            
    def generate_graph_from_csv(self, filepath):
        """Generate interactive graph from CSV data."""
        try:
            self.log("Generating graph from CSV data...")
            
            # Read CSV data
            csvFile_instance = CsvFile()
            articles = csvFile_instance.readData(filepath)
            
            if not articles:
                self.log("No articles found in CSV file.")
                return
            
            df = pd.DataFrame(articles)
            
            if 'Date' in df.columns:
                df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
                df['Year'] = df['Year'].fillna(2020)
            else:
                df['Year'] = range(2015, 2015 + len(df))
            
            # Count articles by label and year
            if 'Label' in df.columns:
                df_counts = df.groupby(['Year', 'Label']).size().reset_index(name='Count')
                
                fig = px.line(df_counts, 
                            x='Year', 
                            y='Count', 
                            color='Label',
                            markers=True,
                            title='Article Distribution by Category Over Time')
                
                fig.update_traces(mode='lines+markers', line_width=3, marker_size=8)
                fig.update_layout(
                    xaxis_title='Year', 
                    yaxis_title='Number of Articles',
                    hovermode='x unified',
                    title_font_size=16,
                    legend_title="Categories",
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                fig.write_html("article_distribution_graph.html")
                self.log("Graph generated and saved as 'article_distribution_graph.html'")
                
                webbrowser.open("article_distribution_graph.html")
            else:
                self.log("No Label column found in CSV. Please run classification first.")
                
        except Exception as e:
            self.log(f"Error generating graph: {e}")
    
    def create_gemini_frame(self):
        """Create the Gemini classification section."""
        gemini_frame = tk.LabelFrame(self.window, text="Gemini AI Classification", padx=10, pady=10)
        gemini_frame.pack(fill="x", padx=10, pady=5)

        file_frame = tk.Frame(gemini_frame)
        file_frame.pack(fill="x", pady=5)
        
        tk.Label(file_frame, text="CSV File:").pack(side=tk.LEFT)
        self.file_entry = tk.Entry(file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(file_frame, text="Browse", 
                              command=self.browse_csv_file)
        browse_btn.pack(side=tk.LEFT)

        params_frame = tk.Frame(gemini_frame)
        params_frame.pack(fill="x", pady=5)
        
        tk.Label(params_frame, text="Topics (comma-separated):").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.topics_entry = tk.Entry(params_frame, width=50)
        self.topics_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(params_frame, text="Min Citations:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.citation_entry = tk.Entry(params_frame, width=10)
        self.citation_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.citation_entry.insert(0, "10")  # Default value

     
        control_frame = tk.Frame(gemini_frame)
        control_frame.pack(fill="x", pady=10)
        
        classify_btn = tk.Button(control_frame, text="Run Gemini Classification", 
                                command=self.run_classification)
        classify_btn.pack(side=tk.LEFT, padx=5)
        
    def create_visualization_frame(self):
        """Create the visualization section."""
        viz_frame = tk.LabelFrame(self.window, text="Visualizations", padx=10, pady=10)
        viz_frame.pack(fill="x", padx=10, pady=5)

        viz_buttons_frame = tk.Frame(viz_frame)
        viz_buttons_frame.pack(fill="x", pady=5)
        
        wordcloud_btn = tk.Button(viz_buttons_frame, text="Generate Word Cloud", 
                                 command=self.generate_wordcloud)
        wordcloud_btn.pack(side=tk.LEFT, padx=5)
        
        graph_btn = tk.Button(viz_buttons_frame, text="Generate Graph", 
                             command=self.generate_graph)
        graph_btn.pack(side=tk.LEFT, padx=5)
        
    def create_fetch_frame(self):
        """Create the fetch articles section."""
        fetch_frame = tk.LabelFrame(self.window, text="Fetch Articles from Scopus", padx=10, pady=10)
        fetch_frame.pack(fill="x", padx=10, pady=5)

        # Fetch parameters
        fetch_params_frame = tk.Frame(fetch_frame)
        fetch_params_frame.pack(fill="x", pady=5)
        
        tk.Label(fetch_params_frame, text="ISSN:").grid(row=0, column=0, sticky="w")
        self.issn_entry = tk.Entry(fetch_params_frame, width=15)
        self.issn_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(fetch_params_frame, text="Start Year:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.start_year_entry = tk.Entry(fetch_params_frame, width=8)
        self.start_year_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(fetch_params_frame, text="End Year:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.end_year_entry = tk.Entry(fetch_params_frame, width=8)
        self.end_year_entry.grid(row=0, column=5, padx=5)

        # Output path
        output_frame = tk.Frame(fetch_frame)
        output_frame.pack(fill="x", pady=5)
        
        tk.Label(output_frame, text="Save As:").pack(side=tk.LEFT)
        self.output_path_entry = tk.Entry(output_frame, width=50)
        self.output_path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_output_btn = tk.Button(output_frame, text="Browse", command=self.browse_save_path)
        browse_output_btn.pack(side=tk.LEFT)

        # Citation limit
        citation_limit_frame = tk.Frame(fetch_frame)
        citation_limit_frame.pack(fill="x", pady=5)
        
        tk.Label(citation_limit_frame, text="Citation Limit:").pack(side=tk.LEFT)
        self.citation_limit_entry = tk.Entry(citation_limit_frame, width=8)
        self.citation_limit_entry.pack(side=tk.LEFT, padx=5)
        self.citation_limit_entry.insert(0, "0")  # Default value

        # Fetch button
        fetch_btn = tk.Button(fetch_frame, text="Fetch Articles", command=self.run_fetch)
        fetch_btn.pack(pady=5)
        
    def create_log_frame(self):
        """Create the log output section."""
        log_frame = tk.LabelFrame(self.window, text="Log Output", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_box = scrolledtext.ScrolledText(log_frame, width=90, height=15)
        self.log_box.pack(fill="both", expand=True)
        
    def create_ui(self):
        """Create the complete user interface."""
     
        title_label = tk.Label(self.window, text="Article Classification Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

    
        self.create_gemini_frame()
        self.create_visualization_frame()
        self.create_fetch_frame()
        self.create_log_frame()

        self.log("1. Fetch articles from Scopus using ISSN and year range")
        self.log("2. Run Gemini classification on your CSV file")
        self.log("3. Generate visualizations (word cloud and graphs)")
        self.log("")
        
    def browse_csv_file(self):
        """Browse for CSV file."""
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
           
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            
    def browse_save_path(self):
        """Browse for save path."""
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:

            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, filename)
            
    def run_classification(self):
        """Run classification in a separate thread."""
        def task():
            self.run_gemini_classification(
                self.file_entry.get(),
                self.topics_entry.get(),
                self.citation_entry.get()
            )
        threading.Thread(target=task, daemon=True).start()
        
    def generate_wordcloud(self):
        """Generate word cloud in a separate thread."""
        def task():
            run_wordcloud(self.file_entry.get(), self.log)
        threading.Thread(target=task, daemon=True).start()
        
    def generate_graph(self):
        """Generate graph in a separate thread."""
        def task():
            self.generate_graph_from_csv(self.file_entry.get())
        threading.Thread(target=task, daemon=True).start()
        
    def run_fetch(self):
        """Run fetch articles in a separate thread."""
        def task():
            self.fetch_articles(
                self.issn_entry.get(),
                self.start_year_entry.get(),
                self.end_year_entry.get(),
                self.output_path_entry.get(),
                self.citation_limit_entry.get()
            )
        threading.Thread(target=task, daemon=True).start()
        
    def run(self):
        """Start the application."""
        self.window.mainloop()


def main():
    """Main entry point."""
    app = ArticleClassifierApp()
    app.run()


if __name__ == "__main__":
    main()
