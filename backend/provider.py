import os
import google.generativeai as genai
from dotenv import load_dotenv

class Provider:
    """Abstraction for configuring and retrieving a Gemini model.
    This follows Sam Bhagwat's principle of provider abstraction.
    """

    def __init__(self):
        # Load environment variables once
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None

    def configure(self):
        """Configure the Gemini client with the API key.
        Can be extended to support multiple providers.
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        genai.configure(api_key=self.api_key)

    def get_model(self, model_name: str = "gemini-2.0-flash-exp"):
        """Return a GenerativeModel instance with function calling tools.
        The caller should add tools after obtaining the model.
        """
        if self.model is None:
            # Model will be created later with tools injected by caller
            self.model = genai.GenerativeModel(model_name=model_name)
        return self.model
