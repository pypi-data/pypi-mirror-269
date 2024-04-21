from bs4 import BeautifulSoup
import requests

class _Base:
    def __init__(self, timeout: int) -> None:
        self.timeout = timeout
        
    def _parse_url(self, url: str) -> BeautifulSoup:
        # clean url
        url.replace(" ", "%20")
        res = requests.get(url, timeout = self.timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup

        