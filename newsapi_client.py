from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import requests
from model import Source, Article, NewsResponse
from const import COUNTRIES, CATEGORIES, LANGUAGES, SORT_METHOD, EVERYTHING_URL
from groq import Groq

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_content(content: str) -> str:
    """
    Summarize the given content using the Groq LLM API in a very short and concise manner,
    focusing on the key points only.
    """
    try:
        # Create chat completion with system and user roles
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please summarize the following article in a very short, concise manner, focusing on the key points only:\n\n{content}"}
            ],
            model="llama-3.3-70b-versatile",
        )
        
        # Log the response to see what is returned from the Groq API
        print("Groq API Response:", response)

        # Extract summary from the response
        if response and "choices" in response:
            choice = response["choices"][0]  # Get the first choice
            summarized_content = choice.get("message", {}).get("content", "")
            
            if summarized_content.strip():  # Check if summary is not empty
                return summarized_content.strip()
        
        # If no valid summary, return the original content
        return content.strip()

    except Exception as e:
        print(f"Summarization failed: {e}")
        return content.strip()



# Fetch the NewsAPI key from environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("API key for NewsAPI is missing. Please set the NEWS_API_KEY environment variable.")

# Initialize the NewsApiClient with the API key
news_client = NewsApiClient(api_key=NEWS_API_KEY)

@app.get("/top-headlines/", response_model=NewsResponse)
async def get_top_headlines(
    category: str = Query(..., title="Category", enum=CATEGORIES),
    country: str = Query(..., title="Country", enum=COUNTRIES),
) -> NewsResponse:
    """
    Fetch the top headlines for a given category and country.
    """
    try:
        results = news_client.get_top_headlines(
            country=country,
            language="en",
            category=category,
            page_size=50,
        )

                # Filter and summarize articles
        filtered_articles = []
        for article in results.get("articles", []):
            if all(article.get(field) != "[Removed]" for field in ["title", "description", "content"]):
                summarized_content = summarize_content(article.get("content")) if article.get("content") else None
                article["content"] = summarized_content  # Replace the original content with the summary
                article["summarizedContent"] = summarized_content  # Add summarized content explicitly
                filtered_articles.append(article)

        results["articles"] = filtered_articles
        

        return NewsResponse(status="ok", totalResults=len(filtered_articles), articles=filtered_articles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching top headlines: {str(e)}")

@app.get("/fetch-articles/", response_model=dict)
async def get_articles(
    q: Optional[str] = Query(None, description="Keywords or phrases to search for in article titles and bodies"),
    language: Optional[str] = Query("en", description="Language of the articles"),
    sortBy: Optional[str] = Query("publishedAt", enum=SORT_METHOD, description="Sort order of the articles"),
    pageSize: Optional[int] = Query(100, description="Number of articles per page"),
    page: Optional[int] = Query(1, description="Page number for pagination"),
    searchIn: Optional[str] = Query(None, description="Fields to search in (e.g., 'title,content')"),
    sources: Optional[str] = Query(None, description="Comma-separated string of source identifiers"),
    domains: Optional[str] = Query(None, description="Comma-separated string of domains to restrict the search to"),
    excludeDomains: Optional[str] = Query(None, description="Comma-separated string of domains to exclude"),
    from_date: Optional[str] = Query(None, description="The earliest article date in ISO 8601 format"),
    to_date: Optional[str] = Query(None, description="The latest article date in ISO 8601 format"),
):
    """
    Fetch articles from the 'everything' endpoint with filtering and summarization.
    """
    try:
        params = {
            "apiKey": NEWS_API_KEY,
            "q": q,
            "language": language,
            "sortBy": sortBy,
            "pageSize": pageSize,
            "page": page,
            "searchIn": searchIn,
            "sources": sources,
            "domains": domains,
            "excludeDomains": excludeDomains,
            "from": from_date,
            "to": to_date,
        }

        # Remove None or empty values from the parameters dictionary
        params = {key: value for key, value in params.items() if value is not None}

        response = requests.get(EVERYTHING_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        articles_data = response.json()

        # Filter and summarize articles
        filtered_articles = []
        for article in articles_data.get("articles", []):
            if all(article.get(field) != "[Removed]" for field in ["title", "description", "content"]):
                summarized_content = summarize_content(article.get("content")) if article.get("content") else None
                article["content"] = summarized_content  # Replace the original content with the summary
                article["summarizedContent"] = summarized_content  # Add summarized content explicitly
                filtered_articles.append(article)

        articles_data["articles"] = filtered_articles
        return articles_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")
