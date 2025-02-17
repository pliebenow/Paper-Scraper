from typing import List, Optional, Dict, Literal

import arxiv
from datetime import datetime
from .paper_scraper import PaperMetadata, PaperScraper

SortOption = Literal["date", "authors", "title", "relevance"]

class ArxivScraper(PaperScraper):
    """Scraper implementation for fetching paper metadata from ArXiv."""

    def __init__(self):
        super().__init__()
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,  # Rate limiting
            num_retries=3
        )
        
        # Mapping of our sort options to ArXiv's sort criteria
        self.sort_criteria = {
            "relevance": arxiv.SortCriterion.Relevance,
            "date": arxiv.SortCriterion.LastUpdatedDate,
            # Authors and title sorting will be handled post-fetch
            # as ArXiv API doesn't support these directly
        }

    async def search_papers(
        self, 
        query: str, 
        max_results: int = 10,
        date_range: Optional[Dict[str, str]] = None,
        sort_by: SortOption = "relevance",
        ascending: bool = False
    ) -> List[PaperMetadata]:
        """
        Search for papers on ArXiv using a query string.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            date_range: Optional dict with 'start_date' and 'end_date' in YYYY-MM-DD format
            sort_by: How to sort the results ("date", "authors", "title", "relevance")
            ascending: Whether to sort in ascending order
            
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

            # Use API-level sorting for supported criteria
            sort_criterion = self.sort_criteria.get(sort_by, arxiv.SortCriterion.Relevance)
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort_criterion
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

            # Handle client-side sorting for unsupported criteria
            if sort_by not in self.sort_criteria:
                papers = self._sort_papers(papers, sort_by, ascending)
            elif not ascending and sort_by == "date":  # ArXiv API returns ascending by default
                papers.reverse()

            return papers

        except Exception as e:
            self.logger.error(f"Error searching ArXiv papers: {str(e)}")
            return []

    def _sort_papers(
        self,
        papers: List[PaperMetadata],
        sort_by: SortOption,
        ascending: bool
    ) -> List[PaperMetadata]:
        """Sort papers by the given criteria"""
        if sort_by == "authors":
            papers.sort(
                key=lambda x: ', '.join(x.authors).lower(),
                reverse=not ascending
            )
        elif sort_by == "title":
            papers.sort(
                key=lambda x: x.title.lower(),
                reverse=not ascending
            )
        return papers

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

