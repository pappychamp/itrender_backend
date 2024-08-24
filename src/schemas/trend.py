from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SiteModel(BaseModel):
    name: str = Field(..., min_length=1, description="SiteName cannot be empty")
    content: str = Field(..., min_length=1, description="Content cannot be empty")


class TagModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="TagName cannot be empty")


class TrendBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title cannot be empty")
    ranking: Optional[int] = Field(None, description="Ranking of the item")
    category: Optional[str] = Field(None, max_length=255, description="Category must be a string with a maximum length of 255 characters")
    published_at: datetime
    url: Optional[str] = Field(None, max_length=255, description="URL must be a string with a maximum length of 255 characters")
    embed_html: Optional[str] = Field(None, description="EmbedHtml must be a string")
    tags: List[TagModel] | None = []


class TrendListResponse(TrendBase):
    site: SiteModel

    model_config = ConfigDict(from_attributes=True)
