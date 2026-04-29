import asyncio
from playwright.async_api import async_playwright
#from playwright_stealth import Stealth
from .config import MAIN_URL, USER_AGENT, EXTRA_HEADERS, MAX_STREAMS
from .parser import AO3parser

class AO3fetcher:
    def __init__(self):
        self.parser = AO3parser()
        self.sem = asyncio.Semaphore(MAX_STREAMS)
        self.playwright = None
        self.browser = None
        self.context = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )
        self.context = await self.browser.new_context(
            user_agent=USER_AGENT, 
            extra_http_headers=EXTRA_HEADERS
        )
        page = await self.context.new_page()
        await page.goto(MAIN_URL)
        await asyncio.sleep(15)
        await page.close()
        print("Контекст готов.")

    async def close(self):
        if self.browser != None and self.playwright != None:
            await self.browser.close()
            await self.playwright.stop()
    

    async def scrape_page_html(self, url: str):
        async with self.sem:
            if self.context != None:
                page = await self.context.new_page()

                await page.route("**/*.{png,jpg,jpeg,css}", lambda route: route.abort())

                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    page_html = await page.content()
                    return page_html
                finally:
                    await page.close()

    #def get_text(self, html_doc: str):
    #    soup = BeautifulSoup(html_doc, 'lxml')

    '''def save_file(self, filename: str, content: str):
        base_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        file_path = data_dir / filename
        
        with open(f"{file_path}.html", "w") as file:
            file.write(content)

        print(f"Файл сохранен в: {file_path}")'''