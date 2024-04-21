import requests
# from requests import HTTPError
import shutil

import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

class ImageItem:
    def __init__(self, dict: dict) -> None:
        # print(dict)
        try:
            self.url = dict["url"]
            self.title = dict["title"]
            self.width = dict["width"]
            self.height = dict["height"]
            self.format = dict["format"]
            if self.url.split(".")[-1] == "jpg":
                self.format = ".jpg"
        except KeyError:
            pass
        pass
    
    def download(self, path = "", filename = None):
        if self.url == "null":
            print("No url provided!")
            return
        if not filename:
            filename = slugify(self.title)
        else:
            filename = slugify(filename)
        
        headers = {'User-Agent': 'mozilla'}
        res = requests.get(self.url, stream=True, headers=headers)
        path = path + filename + self.format
        if res.status_code == 403:
            raise requests.exceptions.HTTPError("Forbidden")

        with open(path, "wb") as f:
            shutil.copyfileobj(res.raw, f)
        del res
        pass
    
    def __str__(self) -> str:
        return {
            "title": self.title,
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "format": self.format}.__str__()