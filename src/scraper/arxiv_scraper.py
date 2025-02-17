from typing import List, Optional, Dict

import arxiv
from datetime import datetime
from .paper_scraper import PaperMetadata, PaperScraper


class ArxivScraper(PaperScraper):
    """Scraper implementation for fetching paper metadata from ArXiv."""

    def __init__(self):
        super().__init__()
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,  # Rate limiting
            num_retries=3
        )

    async def search_papers(
        self, 
        query: str, 
        max_results: int = 10,
        date_range: Optional[Dict[str, str]] = None
    ) -> List[PaperMetadata]:
        """
        Search for papers on ArXiv using a query string.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            date_range: Optional dict with 'start_date' and 'end_date' in YYYY-MM-DD format
            
        Returns:
            List of PaperMetadata objects
        """
        try:
            # Construct date filter if provided
            if date_range:
                date_filter = (
                    f"submittedDate:[{date_range['start_date']} TO {date_range['end_date']}]"
                )
                # Combine with original query
                query = f"{query} AND {date_filter}"

            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            papers = []
            for result in self.client.results(search):
                paper = PaperMetadata(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    publication_date=result.published.strftime("%Y-%m-%d"),
                    doi=None,  # ArXiv papers might not have a DOI
                    url=result.entry_id,
                    citations=None,  # ArXiv API doesn't provide citation count
                    pdf_url=result.pdf_url
                )
                papers.append(paper)

            return papers

        except Exception as e:
            self.logger.error(f"Error searching ArXiv papers: {str(e)}")
            return []

    async def fetch_paper_by_id(self, arxiv_id: str) -> Optional[PaperMetadata]:
        """
        Fetch a specific paper by its ArXiv ID.
        
        Args:
            arxiv_id: The ArXiv ID of the paper
            
        Returns:
            PaperMetadata object if successful, None otherwise
        """
        try:
            search = arxiv.Search(
                id_list=[arxiv_id],
                max_results=1
            )

            results = list(self.client.results(search))
            if results:
                result = results[0]
                return PaperMetadata(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    publication_date=result.published.strftime("%Y-%m-%d"),
                    doi=None,
                    url=result.entry_id,
                    citations=None,
                    pdf_url=result.pdf_url
                )

            return None

        except Exception as e:
            self.logger.error(f"Error fetching ArXiv paper {arxiv_id}: {str(e)}")
            return None

