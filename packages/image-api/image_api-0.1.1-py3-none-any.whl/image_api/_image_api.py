import json
from image_api._base import _Base
import image_api.config as config
from image_api._image_item import ImageItem

# low = 640 x 420
# mid = 1280 x 720
# high = 1920 x 1080


class ImageApi(_Base):
    
    # Image Quality
    quality_map = {
        "low": " 640x420p",
        "mid": " 1280x720p",
        "high": " 1920x1080p"
    }

    
    def __init__(self, timeout: int) -> None:
        super().__init__(timeout)
        self.image_endpoint = config.IMAGE_ENDPOINT
        
    # hidden methods here
    def _extract_images(self, soup) -> dict:
        
        pass

    def search(self, query, quality = "" , count = 10, width: int = None, height: int = None) -> list[ImageItem]:
        """Search for images

        Args:
            query (str): search query
            quality (str, optional): Options (low, medium, high). Defaults to "".
            count (int, optional): Count of image to return (does not affect speed). Defaults to 10.
            width (int, optional): Custom width search. Defaults to None.
            height (int, optional): Custom height search. Defaults to None.

        Returns:
            list[ImageItem]: Returns a list of ``ImageItemDict``
        """
        # handle image quality
        quality = self.quality_map.get(quality, "")
        
        if width and height:
            quality = f"{width}x{height}p"
        soup = self._parse_url(self.image_endpoint + query + quality)

        # this is every single item li
        imgs: list[ImageItem] = []
        
        for item in soup.find_all("li", attrs={"data-idx": True}):
            img_item = item.find("a", attrs={"class": "iusc"})
            name_layer = item.find("a", attrs={"class": "inflnk"})
            img_dimensions = item.find("span", attrs={"class": "nowrap"})
            
            img_dict = {}
            img_url = {}
            img_url['murl'] = "null"
            img_width = "null"
            img_height = "null"
            img_format = "null"
            img_title = "null"

            if img_item:
                img_url = json.loads(img_item["m"])
            
            if img_dimensions:
                img_dimensions = img_dimensions.text.split("·")
                img_width, img_height = img_dimensions[0].split("x")
                img_format = img_dimensions[1].strip()
                
            if name_layer:
                img_title = name_layer["aria-label"]
                
            img_dict = {
                'url': img_url["murl"],
                'title': img_title,
                'width': img_width,
                'height': img_height,
                'format': "." + img_format
            }
            
            imgs.append(ImageItem(img_dict))
        return imgs[:count]
    
    def to_json(self, data: list[ImageItem]):
        """ Convert ImageItem to JSON
        
        Args:
            data (list[ImageItem]): List of ImageItem
            
            Returns:
                Json: JSON representation of ImageItem"""
        

        converted = []
        for img in data:
            converted.append(img.__dict__)
        return converted

        
if __name__ == "__main__":
    api = ImageApi(5)
    api.search("frieren")
    print("done")