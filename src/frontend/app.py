import streamlit as st
import asyncio
from typing import Optional
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.scraper.arxiv_scraper import ArxivScraper

# Initialize scraper
scraper = ArxivScraper()

def run_async(coro):
    """Helper function to run async code in Streamlit"""
    return asyncio.run(coro)

st.set_page_config(
    page_title="ArXiv Paper Search",
    page_icon="📚",
    layout="wide"
)

# Title and description
st.title("📚 ArXiv Paper Search")
st.markdown("""
Search for academic papers on ArXiv. Enter your search query below to get started.
""")

# Search interface
search_col, filter_col = st.columns([3, 1])

with search_col:
    search_query = st.text_input("Enter search terms", 
                                placeholder="e.g., quantum computing")
    
with filter_col:
    max_results = st.number_input("Max results", 
                                 min_value=1, 
                                 max_value=50, 
                                 value=10)

# Search button
if st.button("🔍 Search Papers"):
    if search_query:
        with st.spinner("Searching papers..."):
            # Perform the search
            papers = run_async(scraper.search_papers(search_query, max_results=max_results))
            
            if papers:
                st.success(f"Found {len(papers)} papers")
                
                # Display papers
                for paper in papers:
                    with st.expander(f"📄 {paper.title}"):
                        # Paper metadata
                        st.markdown(f"**Authors:** {', '.join(paper.authors)}")
                        st.markdown(f"**Published:** {paper.publication_date}")
                        
                        # Links
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"[View on ArXiv]({paper.url})")
                        with col2:
                            st.markdown(f"[Download PDF]({paper.pdf_url})")
                        
                        # Abstract
                        st.markdown("**Abstract:**")
                        st.markdown(paper.abstract)
                        
            else:
                st.warning("No papers found matching your search terms.")
    else:
        st.error("Please enter a search query.")

# Sidebar with additional information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application allows you to search for academic papers on ArXiv.
    
    **Features:**
    - Real-time paper search
    - View paper abstracts
    - Download PDFs directly
    - Access original ArXiv pages
    
    **Note:** This application respects ArXiv's rate limits.
    """)
    
    st.header("Search Tips")
    st.markdown("""
    - Use quotes for exact phrases: "quantum computing"
    - Combine terms with AND, OR: quantum AND computing
    - Use parentheses for grouping: (quantum OR classical) AND computing
    """)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using [Streamlit](https://streamlit.io) | "
    "Data from [ArXiv](https://arxiv.org)"
) 