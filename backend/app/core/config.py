from pydantic_settings import BaseSettings
from supabase import create_client, Client

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GEMINI_API_KEY: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()

# Supabase Client'ı global olarak ilklendiriyoruz
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
