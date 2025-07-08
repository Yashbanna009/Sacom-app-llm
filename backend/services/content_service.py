from backend.config import settings
import os

class ContentService:
    def __init__(self):
        # The content directory is one level above the 'backend' directory
        self.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'content')
        self.domain = settings.ACTIVE_DOMAIN

    def get_context(self) -> str:
        """Loads context from the active domain's TXT file."""
        file_path = os.path.join(self.base_path, f"{self.domain}.txt")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Handle cases where the content file for the domain doesn't exist
            return "No specific context available for this domain."
        except Exception as e:
            print(f"Error loading content: {e}")
            return "Error loading context." 