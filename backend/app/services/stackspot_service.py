import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class StackSpotService:
    def __init__(self):
        self.api_key = os.getenv("STACKSPOT_API_KEY")
        self.base_url = os.getenv("STACKSPOT_API_URL", "https://api.stackspot.com/v1")
        
        if not self.api_key:
            raise ValueError("STACKSPOT_API_KEY environment variable is not set")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def call_stackspot_api(
        self, system_prompt: str, data: dict, api_key: Optional[str] = None
    ) -> str:
        """
        Makes an API call to StackSpot AI and returns the response.

        Args:
            system_prompt (str): The instruction/system prompt
            data (dict): Dictionary of variables to format into the user message
            api_key (Optional[str]): Optional custom API key

        Returns:
            str: StackSpot's response text

        Raises:
            Exception: If the API call fails or returns a non-200 status code
        """
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

        # Format the user message with the data
        user_message = self._format_user_message(data)

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0,
            "max_tokens": 4096
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30  # Add timeout
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling StackSpot AI: {str(e)}")

    def _format_user_message(self, data: dict[str, str]) -> str:
        """
        Helper method to format the data into a user message.
        
        Args:
            data (dict[str, str]): Dictionary of data to format
            
        Returns:
            str: Formatted message with XML-like tags
        """
        tag_mapping = {
            "file_tree": "file_tree",
            "readme": "readme",
            "explanation": "explanation",
            "component_mapping": "component_mapping",
            "instructions": "instructions",
            "diagram": "diagram"
        }
        
        parts = []
        for key, value in data.items():
            if key in tag_mapping and (key != "instructions" or value):
                parts.append(f"<{tag_mapping[key]}>\n{value}\n</{tag_mapping[key]}>")
                
        return "\n\n".join(parts)

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a prompt using StackSpot's token counting endpoint.
        Falls back to a simple estimation if the API call fails.

        Args:
            prompt (str): The prompt to count tokens for

        Returns:
            int: Estimated number of tokens
        """
        try:
            response = requests.post(
                f"{self.base_url}/tokenizer/count",
                headers=self.headers,
                json={"text": prompt},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()["token_count"]
        except:
            pass
            
        # Fallback to simple estimation
        # Average English word is about 1.3 tokens
        return int(len(prompt.split()) * 1.3) 