from pydantic import BaseModel
from typing import List, Optional

class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: str
    urlToImage: Optional[str] = None
    publishedAt: str
    content: Optional[str] = None

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]