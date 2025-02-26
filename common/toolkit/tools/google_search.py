"""Module for google search tool implementation"""
import os
import re
import logging
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader


class GoogleSearchManager:
    def __init__(self, api_key=None, search_engine_id=None):
        load_dotenv()

        self.api_key = api_key or os.environ.get('GOOGLE_CLOUD_API_KEY')
        self.search_engine_id = search_engine_id or os.environ.get('GOOGLE_SEARCH_ENGINE_ID')

    def google_search(self, query, num_results=5):
        """Fetches search results using Google Custom Search API."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.api_key,
            "cx": self.search_engine_id,
            "num": num_results,
        }

        response = requests.get(url, params=params, timeout=60)
        if response.status_code == 200:
            return response.json().get("items", [])

        logging.error("Error: %s %s", response.status_code, response.text)
        return []

    def fetch_page_content_with_langchain(self, url):
        """Fetches the full page content using Langchain's WebBaseLoader."""
        loader = WebBaseLoader([url])
        documents = loader.load()
        return str(documents)

    def clean_text(self, text):
        # Remove unwanted characters using regex
        # This pattern removes newlines, tabs, and multiple spaces
        cleaned = re.sub(r'[\n\t\r]+', ' ', text)  # Replace newlines and tabs with a space
        cleaned = re.sub(r'[^\w\s,.!?-]', '', cleaned)  # special characters
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Replace multiple spaces with a single space
        cleaned = cleaned.strip()  # Remove leading and trailing whitespace
        return cleaned

    def get_google_search_data(self, query: str):
        """Performs a Google search and fetches detailed content."""
        results = self.google_search(query, 5)
        context = []

        if results:
            for idx, item in enumerate(results, 1):
                title = item.get("title")
                snippet = item.get("snippet")
                url = item.get("link")

                logging.info("\n%s. %s\n%s\n%s\n", idx, title, snippet, url)

                # Extract full page content
                detailed_content = self.fetch_page_content_with_langchain(url)
                cleaned_data = self.clean_text(detailed_content)

                logging.info(f"Extracted Content:\n{cleaned_data[:100]}...\n{'-'*80}")
                context.append({
                    'title': title,
                    'snippet': snippet,
                    'url': url,
                    'context': cleaned_data
                })

        return str(context)
