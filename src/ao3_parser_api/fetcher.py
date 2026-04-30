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
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    

    async def scrape_page_html(self, url: str):
        async with self.sem:
            if self.context is None:
                print("Контекст не создан! Вызовите start()")
                return None
            
            page = await self.context.new_page()

            await page.route("**/*.{png,jpg,jpeg,css}", lambda route: route.abort())

            try:
                await asyncio.wait_for(page.goto(url, wait_until="domcontentloaded"), timeout=60.0)
                page_html = await page.content()
                return page_html
            except Exception as e:
                print(f"Ошибка загрузки {url}: {type(e).__name__} - {e}")
                return None
            finally:
                await page.close()