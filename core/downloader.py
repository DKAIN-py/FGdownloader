import os
import time
import asyncio
import aiohttp
import aiofiles
import psutil
import requests
from lxml import html
from PySide6.QtCore import QObject, Signal

from config import FUCKING_FAST_DOWNLOAD_BUTTON_XPATH, TIMEOUT

class DownloadWorker(QObject):
    progress_update = Signal(str, int, int)
    status_update = Signal(str)
    download_finished = Signal()
    download_error = Signal(str)

    def __init__(self, links, download_dir, internet_speed_mbps=30, speed_limit_mbps=None, priority="Normal", use_async=True):
        super().__init__()
        self.links = links
        self.download_dir = download_dir
        self.internet_speed_mbps = internet_speed_mbps
        self.speed_limit_mbps = speed_limit_mbps
        self.priority = priority
        self.use_async = use_async

    def apply_traffic_priorities(self):
        """Sets Windows process priority to give the app network/CPU priority."""
        try:
            p = psutil.Process(os.getpid())
            if self.priority == "High":
                p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            else:
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
        except Exception:
            pass

    def get_final_download_url(self, page_url):
        """
        Validates the URL using the download button XPath and extracts the file URL.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        try:
            response = requests.get(page_url, headers=headers, timeout=TIMEOUT)
            if response.status_code != 200:
                return None
            print(f"Raw content: {response.content}\n\n")
            tree = html.fromstring(response.content)
            print(f"Tree: {tree}\n\n")
            # Validate with your exact XPath
            button_nodes = tree.xpath(FUCKING_FAST_DOWNLOAD_BUTTON_XPATH)
            
            if not button_nodes:
                # Validation failed (Wrong site or ad redirect)
                return None

            # Get the form or direct link that begins the file download
            form_nodes = tree.xpath('//form[@action]')
            if form_nodes:
                return form_nodes[0].get('action')
                
            # Fallback for anchor links
            download_links = tree.xpath('//a[contains(@class, "download")]/@href')
            if download_links:
                return download_links[0]
                
        except Exception as e:
            self.download_error.emit(f"Validation error for {page_url}: {str(e)}")
            
        return None

    async def download_chunked_with_resume(self, session, item, save_path):
        """Downloads the file with resume capabilities and tracks progress."""
        headers = {}
        if os.path.exists(save_path):
            downloaded_bytes = os.path.getsize(save_path)
            headers['Range'] = f'bytes={downloaded_bytes}-'
        else:
            downloaded_bytes = 0

        # Resolve the actual file endpoint on FuckingFast
        direct_url = self.get_final_download_url(item['url'])
        if not direct_url:
            self.download_error.emit(f"Failed to validate the download link for {item['name']}. Invalid webpage or ad detected.")
            return

        async with session.get(direct_url, headers=headers) as response:
            if response.status in [200, 206]:
                total_bytes = int(response.headers.get('Content-Length', 0)) + downloaded_bytes
                mode = 'ab' if downloaded_bytes > 0 else 'wb'
                
                async with aiofiles.open(save_path, mode) as f:
                    async for chunk in response.content.iter_chunked(64 * 1024):
                        await f.write(chunk)
                        downloaded_bytes += len(chunk)
                        
                        # Match current progress with the filename being processed
                        self.progress_update.emit(item['name'], downloaded_bytes, total_bytes)
                        
                        if self.speed_limit_mbps:
                            await asyncio.sleep(len(chunk) / (self.speed_limit_mbps * 125000))
            else:
                self.download_error.emit(f"Server returned status {response.status} for {item['name']}")

    async def download_with_semaphore(self, session, item, semaphore):
        async with semaphore:
            save_path = os.path.join(self.download_dir, item['name'])
            await self.download_chunked_with_resume(session, item, save_path)

    async def run_downloads(self):
        self.apply_traffic_priorities()
        os.makedirs(self.download_dir, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            if self.use_async:
                self.status_update.emit("High-speed network connection detected: Running in Async Mode")
                semaphore = asyncio.Semaphore(3)
                tasks = [self.download_with_semaphore(session, item, semaphore) for item in self.links]
                await asyncio.gather(*tasks)
            else:
                self.status_update.emit("Standard connection detected: Running in Sequential Mode")
                for item in self.links:
                    save_path = os.path.join(self.download_dir, item['name'])
                    await self.download_chunked_with_resume(session, item, save_path)

            self.download_finished.emit()

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_downloads())
        finally:
            loop.close()

def check_internet_speed_mbps(test_url="https://speed.hetzner.de/100MB.bin", timeout=3):
    """
    Downloads a small portion of a test file to calculate the current download speed in Mbps.
    """
    try:
        start_time = time.time()
        headers = {"Range": "bytes=0-1048576"} 
        response = requests.get(test_url, headers=headers, timeout=timeout)
        
        duration = time.time() - start_time
        
        if response.status_code in [200, 206]:
            size_bits = len(response.content) * 8
            speed_bps = size_bits / duration
            speed_mbps = speed_bps / (1024 * 1024)
            return round(speed_mbps, 2)
    except Exception:
        pass
    
    return 15.0