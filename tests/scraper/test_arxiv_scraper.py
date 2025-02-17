"""Tests for the ArXiv paper scraping functionality."""

from pathlib import Path
import sys
from typing import List

import pytest
from src.scraper.arxiv_scraper import ArxivScraper
from src.scraper.paper_scraper import PaperMetadata

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)


@pytest.fixture
def test_scraper():
    """Fixture that provides an ArxivScraper instance for testing."""
    return ArxivScraper()


@pytest.mark.asyncio
async def test_search_papers_basic(test_scraper):
    """Test basic paper search functionality"""
    papers = await test_scraper.search_papers(
        "quantum computing",
        max_results=2
    )
    assert len(papers) <= 2
    assert all(isinstance(paper, PaperMetadata) for paper in papers)
    
    for paper in papers:
        assert paper.title
        assert isinstance(paper.authors, list)
        assert paper.abstract
        assert paper.publication_date
        assert paper.url
        assert paper.pdf_url


@pytest.mark.asyncio
async def test_search_papers_empty_query(test_scraper):
    """Test search with empty query"""
    papers = await test_scraper.search_papers("")
    assert len(papers) == 0


@pytest.mark.asyncio
async def test_search_papers_invalid_query(test_scraper):
    """Test search with invalid query"""
    papers = await test_scraper.search_papers(
        "thisisaverylongandinvalidquerythatshouldfailxxxxxxxxxxx" * 10
    )
    assert len(papers) == 0


@pytest.mark.asyncio
async def test_fetch_paper_by_id_valid(test_scraper):
    """Test fetching a known paper by ID"""
    # Using a known ArXiv paper ID
    paper = await test_scraper.fetch_paper_by_id("2103.13916")
    
    assert paper is not None
    assert isinstance(paper, PaperMetadata)
    assert paper.title
    assert len(paper.authors) > 0
    assert paper.abstract
    assert paper.publication_date
    assert paper.url
    assert paper.pdf_url


@pytest.mark.asyncio
async def test_fetch_paper_by_id_invalid(test_scraper):
    """Test fetching paper with invalid ID"""
    paper = await test_scraper.fetch_paper_by_id("0000.00000")
    assert paper is None


@pytest.mark.asyncio
async def test_search_papers_max_results(test_scraper):
    """Test max_results parameter"""
    max_results = 5
    papers = await test_scraper.search_papers(
        "physics",
        max_results=max_results
    )
    assert len(papers) <= max_results


@pytest.mark.asyncio
async def test_paper_metadata_structure(test_scraper):
    """Test structure of returned PaperMetadata"""
    papers = await test_scraper.search_papers(
        "machine learning",
        max_results=1
    )
    
    assert len(papers) == 1
    paper = papers[0]
    
    # Check all fields are present and have correct types
    assert isinstance(paper.title, str)
    assert isinstance(paper.authors, list)
    assert isinstance(paper.abstract, str)
    assert isinstance(paper.publication_date, str)
    assert isinstance(paper.url, str)
    assert isinstance(paper.pdf_url, str)
    assert paper.doi is None  # ArXiv papers typically don't have DOIs
    assert paper.citations is None  # Citations not provided by ArXiv API