# Technical Documentation: ArXiv Scraper

## Overview
This document outlines the architecture and technical details of the **ArXiv Scraper** application, which fetches academic papers from ArXiv and presents them via a stateless web frontend.

## Architecture
The application consists of two main components:

1. **Frontend**: A **Streamlit** web UI that allows users to search for and display research papers.
2. **Backend**: A **Python-based API (FastAPI/Flask)** that fetches and processes data from ArXiv.

The application is entirely **stateless**, meaning no persistent database is used. Data is retrieved in real-time and presented to the user without long-term storage.

### Components
- **Frontend**: Built with Streamlit, interacting with the backend via API calls.
- **Backend**: A lightweight Python API using FastAPI or Flask to fetch and serve ArXiv data.
- **ArXiv API**: The external data source for retrieving research papers.

## Technology Stack
| Component  | Technology   |
|------------|-------------|
| Frontend   | Streamlit   |
| Backend    | FastAPI/Flask |
| Data Source | ArXiv API   |

## API Endpoints
### `GET /search?query=<search_term>`
- **Description**: Fetches papers related to the given search term from ArXiv.
- **Response**:
  ```json
  {
    "papers": [
      {
        "title": "Example Paper Title",
        "authors": ["Author 1", "Author 2"],
        "abstract": "This is a summary of the paper...",
        "url": "https://arxiv.org/abs/1234.56789"
      }
    ]
  }
  ```

## Deployment
### Local Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/example/arxiv-scraper.git
   cd arxiv-scraper
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the backend:
   ```sh
   uvicorn app:app --reload  # For FastAPI
   python app.py  # For Flask
   ```
4. Run the frontend:
   ```sh
   streamlit run frontend.py
   ```

## Notes
- The application **does not store any data**; all information is fetched in real-time.
- Future enhancements may include caching results temporarily for performance improvements.

## License
This project is open-source under the MIT License.