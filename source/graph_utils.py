import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from labelUtilities import CategoryHandler
from entryUtilities import CsvFile
import scopus_data
from gemini import geminiClassify
from wordcloud_graph import run_wordcloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import re
import ast
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from PIL import Image, ImageTk

def fetch_articles(issn, start_year, end_year, output_path, citation_limit=0, log_callback=None):
    try:
        if log_callback: log_callback(f"Fetching articles for ISSN {issn} from {start_year} to {end_year}...")
        scopus_instance = scopus_data.ScopusData()
        years = scopus_data.yearsArray(int(start_year), int(end_year))
        citation_limit = int(citation_limit) if citation_limit else 0

        journal = scopus_instance.getJournal(issn, years, citation_limit)

        csv_instance = CsvFile()
        csv_instance.writeDataArticles(output_path, journal.articles)

        if log_callback: log_callback(f"{len(journal.articles)} articles written to: {output_path}")
    except Exception as e:
        if log_callback: log_callback(f"Error: {e}")
        else: print(e)
        
def run_gemini_classification(filepath, topics, citation_threshold, log_callback):
    def task():
        try:
            topics_list = topics.split(",") if topics else []
            log_callback("Running Gemini classification...")

            articles = geminiClassify(filepath, topics_list, citation_threshold)
            categoryCountDict = CategoryHandler.categoryCount(articles)
            CategoryHandler.writeCategory(categoryCountDict, filepath)
            log_callback("Gemini classification complete.")
        except Exception as e:
            log_callback(f"Error: {e}")
    threading.Thread(target=task).start()

def run_fetch_articles(issn, start_year, end_year, output_path, citation_limit, log_callback):
    def task():
        fetch_articles(issn, start_year, end_year, output_path, citation_limit, log_callback)
    threading.Thread(target=task).start()

def generate_graph_from_csv(filepath, log_callback):
    """Generate graph from CSV data and display in the application"""
    def task():
        try:
            log_callback("Generating graph from CSV data...")
            
           
            csvFile_instance = CsvFile()
            articles = csvFile_instance.readData(filepath)
            
            if not articles:
                log_callback("No articles found in CSV file.")
                return
            
        
            df = pd.DataFrame(articles)
            
           
            if 'Date' in df.columns:
                df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
            else:
              
                df['Year'] = range(2015, 2015 + len(df))
        
          
            if 'Label' in df.columns:
                df_counts = df.groupby(['Year', 'Label']).size().reset_index(name='Count')
                
            
                fig = px.line(df_counts, 
                            x='Year', 
                            y='Count', 
                            color='Label',
                            markers=True,
                            title='Article Distribution by Category Over Time')
                
                fig.update_traces(mode='lines+markers')
                fig.update_layout(xaxis_title='Year', yaxis_title='Number of Articles')
                
               
                fig.write_html("temp_graph.html")
                log_callback("Graph generated and saved as 'temp_graph.html'")
                
               
                import webbrowser
                webbrowser.open("temp_graph.html")
            else:
                log_callback("No Label column found in CSV. Please run classification first.")
                
        except Exception as e:
            log_callback(f"Error generating graph: {e}")
    
    threading.Thread(target=task).start()

def create_ui():
    window = tk.Tk()
    window.title("Article Classification Tool")
    window.geometry("900x800")
    
 
    style = ttk.Style()
    style.theme_use('clam')
    
    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    
    title_label = tk.Label(window, text="Article Classification Tool", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)


    gemini_frame = tk.LabelFrame(window, text="Gemini AI Classification", padx=10, pady=10)
    gemini_frame.pack(fill="x", padx=10, pady=5)

 
    file_frame = tk.Frame(gemini_frame)
    file_frame.pack(fill="x", pady=5)
    
    tk.Label(file_frame, text="CSV File:").pack(side=tk.LEFT)
    file_entry = tk.Entry(file_frame, width=50)
    file_entry.pack(side=tk.LEFT, padx=5)
    
    browse_btn = tk.Button(file_frame, text="Browse", 
                          command=lambda: file_entry.insert(0, filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])))
    browse_btn.pack(side=tk.LEFT)


    params_frame = tk.Frame(gemini_frame)
    params_frame.pack(fill="x", pady=5)
    
    tk.Label(params_frame, text="Topics (comma-separated):").grid(row=0, column=0, sticky="w", padx=(0, 5))
    topics_entry = tk.Entry(params_frame, width=50)
    topics_entry.grid(row=0, column=1, padx=5)
    
    tk.Label(params_frame, text="Min Citations:").grid(row=1, column=0, sticky="w", padx=(0, 5))
    citation_entry = tk.Entry(params_frame, width=10)
    citation_entry.grid(row=1, column=1, sticky="w", padx=5)
    citation_entry.insert(0, "10") 

 
    control_frame = tk.Frame(gemini_frame)
    control_frame.pack(fill="x", pady=10)
    
    classify_btn = tk.Button(control_frame, text="Run Gemini Classification", 
                            command=lambda: run_gemini_classification(
                                file_entry.get(),
                                topics_entry.get(),
                                citation_entry.get(),
                                log
                            ))
    classify_btn.pack(side=tk.LEFT, padx=5)

 
    viz_frame = tk.LabelFrame(window, text="Visualizations", padx=10, pady=10)
    viz_frame.pack(fill="x", padx=10, pady=5)

    viz_buttons_frame = tk.Frame(viz_frame)
    viz_buttons_frame.pack(fill="x", pady=5)
    
    wordcloud_btn = tk.Button(viz_buttons_frame, text="Generate Word Cloud", 
                             command=lambda: run_wordcloud(file_entry.get(), log))
    wordcloud_btn.pack(side=tk.LEFT, padx=5)
    
    graph_btn = tk.Button(viz_buttons_frame, text="Generate Graph", 
                         command=lambda: generate_graph_from_csv(file_entry.get(), log))
    graph_btn.pack(side=tk.LEFT, padx=5)


    fetch_frame = tk.LabelFrame(window, text="Fetch Articles from Scopus", padx=10, pady=10)
    fetch_frame.pack(fill="x", padx=10, pady=5)

  
    fetch_params_frame = tk.Frame(fetch_frame)
    fetch_params_frame.pack(fill="x", pady=5)
    
    tk.Label(fetch_params_frame, text="ISSN:").grid(row=0, column=0, sticky="w")
    issn_entry = tk.Entry(fetch_params_frame, width=15)
    issn_entry.grid(row=0, column=1, padx=5)
    
    tk.Label(fetch_params_frame, text="Start Year:").grid(row=0, column=2, sticky="w", padx=(10, 0))
    start_year_entry = tk.Entry(fetch_params_frame, width=8)
    start_year_entry.grid(row=0, column=3, padx=5)
    
    tk.Label(fetch_params_frame, text="End Year:").grid(row=0, column=4, sticky="w", padx=(10, 0))
    end_year_entry = tk.Entry(fetch_params_frame, width=8)
    end_year_entry.grid(row=0, column=5, padx=5)

  
    output_frame = tk.Frame(fetch_frame)
    output_frame.pack(fill="x", pady=5)
    
    tk.Label(output_frame, text="Save As:").pack(side=tk.LEFT)
    output_path_entry = tk.Entry(output_frame, width=50)
    output_path_entry.pack(side=tk.LEFT, padx=5)
    
    def browse_save_path():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, filename)
    
    browse_output_btn = tk.Button(output_frame, text="Browse", command=browse_save_path)
    browse_output_btn.pack(side=tk.LEFT)

  
    citation_limit_frame = tk.Frame(fetch_frame)
    citation_limit_frame.pack(fill="x", pady=5)
    
    tk.Label(citation_limit_frame, text="Citation Limit:").pack(side=tk.LEFT)
    citation_limit_entry = tk.Entry(citation_limit_frame, width=8)
    citation_limit_entry.pack(side=tk.LEFT, padx=5)
    citation_limit_entry.insert(0, "0")  

   
    fetch_btn = tk.Button(fetch_frame, text="Fetch Articles", 
                         command=lambda: run_fetch_articles(
                             issn_entry.get(),
                             start_year_entry.get(),
                             end_year_entry.get(),
                             output_path_entry.get(),
                             citation_limit_entry.get(),
                             log
                         ))
    fetch_btn.pack(pady=5)

    # Log Frame 
    log_frame = tk.LabelFrame(window, text="Log Output", padx=10, pady=10)
    log_frame.pack(fill="both", expand=True, padx=10, pady=5)

    log_box = scrolledtext.ScrolledText(log_frame, width=90, height=15)
    log_box.pack(fill="both", expand=True)

  
    log("Welcome to Article Classification Tool - Gemini Edition!")
    log("1. Fetch articles from Scopus using ISSN and year range")
    log("2. Run Gemini classification on your CSV file")
    log("3. Generate visualizations (word cloud and graphs)")
    log("")

    window.mainloop()

if __name__ == "__main__":
    create_ui()
