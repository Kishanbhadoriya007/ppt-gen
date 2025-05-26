# app/schemas.py
from pydantic import BaseModel, Field, FilePath, HttpUrl
from typing import List, Optional, Dict
from fastapi import UploadFile

class SlideContentRequest(BaseModel):
    heading: str
    prompt: str # User can refine this based on the heading
    tokens_per_slide: int = Field(default=250, ge=50, le=8192) # Max tokens for this slide's content
    style_tone: Optional[str] = "neutral" # e.g., formal, casual, academic
    content_format: Optional[str] = "bullet_points" # e.g., summary, paragraph

class PresentationConfig(BaseModel):
    main_topic: str
    num_slides: int = Field(default=5, ge=1, le=10)
    template_choice: str # 'upload' or 'server_template_filename.pptx'
    theme_color: Optional[str] = None # VIBGYOR or RGB hex
    max_tokens_per_slide: int = Field(default=250, ge=50, le=500)
    style_tone: Optional[str] = "neutral"
    content_format: Optional[str] = "bullet_points" # Default for all slides, can be overridden

class SlideHeading(BaseModel):
    id: int
    heading: str
    editable: bool = True

class GeneratedHeadingsResponse(BaseModel):
    main_topic: str
    num_slides: int
    headings: List[SlideHeading]
    session_id: str # To track the generation process

class FinalPresentationRequest(BaseModel):
    session_id: str
    final_headings: List[str] # User can edit these
    template_choice: str
    uploaded_template_path: Optional[str] = None # Path if user uploaded
    server_template_name: Optional[str] = None # Filename if server template
    theme_color: Optional[str] = None
    max_tokens_per_slide: int
    style_tone: str
    content_format: str
    placeholder_map: Optional[Dict[int, Dict[str, int]]] = None # {slide_idx: {"title": placeholder_idx, "content": placeholder_idx}}

class JobStatus(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None
    download_url: Optional[HttpUrl] = None