from typing import TypedDict, Optional
from pydantic import BaseModel, Field


class Blog(BaseModel):
    title: str = Field(description="The title of the blog post")
    content: str = Field(description="The main content of the blog post in Markdown format")


class BlogState(TypedDict):
    topic: str
    blog: Blog
    current_language: str
    feedback: Optional[str]        
    iteration: int                  