from config import XPATH, TIMEOUT
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from lxml import html
import requests
import re 
from PySide6.QtCore import QThread, Signal 

class FetchThread(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url:str):
        super().__init__()
        self.url = url

    def run(self) -> dict:
        try:
            try:
                response = requests.get(self.url, timeout=TIMEOUT)
                response.raise_for_status()
            except HTTPError as e:
                return {"Http Error": e}
            except ConnectionError as e:
                return {"Connection Error": e}
            except Timeout as t:
                return {"Timeout Error": t}
            except RequestException as e:
                return {"Request Error": e}

            tree = html.fromstring(response.content)
            container = tree.xpath(XPATH)

            if not container:
                self.error.emit("Could not locate the direct links section on this page. Verify the URL.")
                return

            base, optional = [], []
            opt_regex = re.compile(r'^(fg-optional|fg-selective)')

            elements = container[0].xpath('.//a')
            for ele in elements:
                href = ele.get('href')
                text = ele.text_content().strip()

                if opt_regex.search(text):
                    optional.append({"name": text, "url": href})
                else:
                    base.append({"name": text, "url": href})

            self.finished.emit({"base": base, "optional": optional})

        except Exception as e:
            self.error.emit(f"Error fetching page {e}")

