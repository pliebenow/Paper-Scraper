# ArXiv Paper Scraper

A stateless web application that allows users to search and fetch academic papers from ArXiv using a modern Python stack.

## 🚀 Features

- Real-time paper search and retrieval from ArXiv
- Clean and intuitive Streamlit web interface
- FastAPI backend for efficient API handling
- Stateless architecture with no database requirements
- Rate-limited API interactions to respect ArXiv's guidelines
- Comprehensive test coverage

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Data Source**: ArXiv API
- **Testing**: pytest, pytest-asyncio
- **Code Quality**: mypy, black

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/arxiv-scraper.git
cd arxiv-scraper
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

1. Start the backend server:
```bash
uvicorn src.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run src/frontend/app.py
```

3. Open your browser and navigate to:
- Frontend: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## 🧪 Running Tests

Run the test suite:
```bash
pytest tests/ -v
```

Run tests with coverage report:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## 📁 Project Structure

```
arxiv-scraper/
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── paper_scraper.py
│   │   └── arxiv_scraper.py
│   ├── frontend/
│   │   └── app.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── scraper/
│       └── test_arxiv_scraper.py
├── docs/
│   ├── status.md
│   ├── technical.md
│   └── tasks.md
├── requirements.txt
└── README.md
```

## 🔍 API Endpoints

### GET /search
Search for papers on ArXiv.

**Parameters:**
- `query` (string): Search query
- `max_results` (int, optional): Maximum number of results to return (default: 10)

**Response:**
```json
{
  "papers": [
    {
      "title": "Example Paper Title",
      "authors": ["Author 1", "Author 2"],
      "abstract": "Paper abstract...",
      "url": "https://arxiv.org/abs/...",
      "pdf_url": "https://arxiv.org/pdf/..."
    }
  ]
}
```

### GET /paper/{paper_id}
Fetch a specific paper by ID.

**Parameters:**
- `paper_id` (string): ArXiv paper ID

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- ArXiv for providing the API
- The Python community for the excellent tools and libraries

## ⚠️ Note

This application respects ArXiv's rate limits and usage guidelines. Please use responsibly. 