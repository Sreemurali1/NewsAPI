# NewsAPI Project using FastAPI

## Introduction
This project is a **FastAPI-based NewsAPI** that allows users to fetch the latest news articles from various sources. It provides endpoints for retrieving news based on categories, keywords, and sources.

## Features
- Fetch news articles from multiple sources
- Filter news by category, keyword, or country
- FastAPI integration with async processing
- Simple and efficient API design
- JSON-based responses

## Technologies Used
- **FastAPI** - For building the API
- **Requests** - For making external API calls
- **Pydantic** - For request validation
- **Uvicorn** - For running the FastAPI server
- **NewsAPI.org** - As the external news data provider

## Installation

### Prerequisites
- Python 3.8+
- NewsAPI API Key (https://newsapi.org/)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Sreemurali1/NewsAPI.git
   cd newsapi-fastapi
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```sh
   export NEWSAPI_KEY=your_api_key_here  # On Windows use `set NEWSAPI_KEY=your_api_key_here`
   ```

5. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

### 1. Get Top Headlines
```http
GET /news/top-headlines
```
**Query Parameters:**
- `country`: Filter by country (e.g., `us`, `in`)
- `category`: Filter by category (e.g., `business`, `sports`)
- `q`: Search keyword

### 2. Get Everything
```http
GET /news/everything
```
**Query Parameters:**
- `q`: Search keyword
- `sources`: Filter by source (e.g., `bbc-news`, `cnn`)
- `from_date`: Start date (YYYY-MM-DD)
- `to_date`: End date (YYYY-MM-DD)

## Example Usage
Fetching top headlines for India:
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/news/top-headlines?country=in' \
  -H 'accept: application/json'
```


## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to the branch and submit a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, reach out to **sreemuralislm@gmail.com**

