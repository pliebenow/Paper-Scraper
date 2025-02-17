from typing import List, Optional

import arxiv
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
        self, query: str, max_results: int = 10
    ) -> List[PaperMetadata]:
        """Search for papers on ArXiv using a query string."""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            papers = []
            # arxiv.Client.results() returns an iterator, not an awaitable
            results = self.client.results(search)  # Remove await
            for result in results:
                paper = PaperMetadata(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    publication_date=result.published.strftime("%Y-%m-%d"),
                    doi=None,  # ArXiv papers might not have a DOI
                    url=result.entry_id,
                    citations=None,
                    pdf_url=result.pdf_url
                )
                papers.append(paper)

            return papers

        except arxiv.ArxivError as e:
            self.logger.error(
                "Error searching ArXiv papers: %s", 
                str(e)
            )
            return []

    async def fetch_paper_by_id(
        self, arxiv_id: str
    ) -> Optional[PaperMetadata]:
        """Fetch a specific paper by its ArXiv ID."""
        try:
            search = arxiv.Search(
                id_list=[arxiv_id],
                max_results=1
            )

            # arxiv.Client.results() returns an iterator, not an awaitable
            results = self.client.results(search)  # Remove await
            for result in results:
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

        except arxiv.ArxivError as e:
            self.logger.error(
                "Error fetching ArXiv paper %s: %s",
                arxiv_id,
                str(e)
            )
            return None

