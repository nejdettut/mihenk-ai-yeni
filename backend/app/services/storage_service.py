from app.core.config import supabase
import os

class StorageService:
    BUCKET = "exam-photos"

    @staticmethod
    async def upload_exam_photo(content: bytes, file_name: str) -> str:
        """Uploads bytes to Supabase storage and returns a public URL."""
        return await StorageService.upload_file(content, file_name, StorageService.BUCKET)

    @staticmethod
    async def upload_file(content: bytes, file_name: str, bucket: str) -> str:
        """Generic upload helper for Supabase storage."""
        # In test mode, write locally instead of uploading
        if os.getenv("TEST_MODE") == "1":
            local_dir = os.path.join(os.getcwd(), "tmp", "uploads")
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, file_name)
            with open(local_path, "wb") as f:
                f.write(content)
            return f"file://{local_path}"

        resp = supabase.storage.from_(bucket).upload(file_name, content)
        if isinstance(resp, dict) and resp.get("error"):
            raise Exception(f"Storage upload failed: {resp['error']}")

        url_resp = supabase.storage.from_(bucket).get_public_url(file_name)
        if isinstance(url_resp, dict):
            return url_resp.get("publicURL") or url_resp.get("public_url") or url_resp.get("url")
        return url_resp
