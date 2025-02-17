"""Streamlit web application for searching and displaying ArXiv papers."""

import streamlit as st
import asyncio
from typing import Optional
import sys
from pathlib import Path
from datetime import datetime, timedelta

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
    search_query = st.text_input(
        "Enter search terms",
        placeholder="e.g., quantum computing"
    )
    
    # Date range filters
    date_col1, date_col2 = st.columns(2)
    
    with date_col1:
        earliest_date = st.date_input(
            "Earliest Date",
            value=datetime.now() - timedelta(days=365),  # Default to 1 year ago
            min_value=datetime(1991, 8, 14),  # ArXiv's launch date
            max_value=datetime.now()
        )
    
    with date_col2:
        latest_date = st.date_input(
            "Latest Date",
            value=datetime.now(),
            min_value=datetime(1991, 8, 14),
            max_value=datetime.now()
        )

with filter_col:
    max_results = st.number_input(
        "Max results",
        min_value=1,
        max_value=50,
        value=10
    )

# Validate date range
if earliest_date > latest_date:
    st.error("Earliest date must be before latest date")
    st.stop()

# Search button
if st.button("🔍 Search Papers"):
    if search_query:
        with st.spinner("Searching papers..."):
            # Convert dates to strings in the format YYYY-MM-DD
            date_range = {
                'start_date': earliest_date.strftime('%Y-%m-%d'),
                'end_date': latest_date.strftime('%Y-%m-%d')
            }
            
            # Perform the search with date range
            papers = run_async(scraper.search_papers(
                search_query, 
                max_results=max_results,
                date_range=date_range
            ))
            
            if papers:
                # Filter papers by date
                filtered_papers = [
                    paper for paper in papers
                    if earliest_date <= datetime.strptime(paper.publication_date, '%Y-%m-%d').date() <= latest_date
                ]
                
                st.success(f"Found {len(filtered_papers)} papers within the specified date range")
                
                # Display papers
                for paper in filtered_papers:
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
                st.warning("No papers found matching your search terms and date range.")
    else:
        st.error("Please enter a search query.")

# Sidebar with additional information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application allows you to search for academic papers on ArXiv.
    **Features:**
    - Real-time paper search
    - Date range filtering
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
    - Use date range to narrow down results
    """)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using [Streamlit](https://streamlit.io) | "
    "Data from [ArXiv](https://arxiv.org)"
)