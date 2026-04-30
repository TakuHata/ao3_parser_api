from ao3_parser_api.fetcher import AO3fetcher
from ao3_parser_api.parser import AO3parser
from ao3_parser_api.saver import AO3saver
from .config import URLS, CHUNK_SIZE
from .datatype import FicData
import asyncio

async def main():
    print('Running AO3 Parser API...')
    fetcher = AO3fetcher()
    parser = AO3parser()
    saver = AO3saver()

    #with open("C:\\Users\\Takumi\\Documents\\FFN API\\ao3_parser_api\\example.html", "r", encoding="utf-8") as f:
    #    file = f.read()

    try:
        await fetcher.start()

        all_fic_data: list[FicData] = []

        for i in range(0, len(URLS), CHUNK_SIZE):
            chunk = URLS[i:i+CHUNK_SIZE]
            html_chunk = await asyncio.gather(
                *[fetcher.scrape_page_html(url) for url in chunk],
                return_exceptions=True
            )


            for url, html in zip(chunk, html_chunk):
                if isinstance(html, Exception):
                    print(f"Ошибка при загрузке {url}: {html}")
                    continue
                if html is None:
                    print(f"Пустой результат для {url}")
                    continue
                try:
                    fics: list[FicData] = parser.get_works(str(html), 2)
                    all_fic_data.extend(fics)
                except Exception as e:
                    print(f"Ошибка парсинга HTML для {url}: {e}")
                    continue


            print(f"Обработано страниц: {min(i+CHUNK_SIZE, len(URLS))} из {len(URLS)}, всего фиков: {len(all_fic_data)}")

        sql_tuples = parser.convert_to_tuple(all_fic_data)

        try:
            await asyncio.wait_for(asyncio.to_thread(saver.save_json_db, all_fic_data), timeout=600.0)
            print("JSON сохранён успешно")
        except Exception as e:
            print(f"Ошибка сохранения JSON: {e}")
            

        try:
            await asyncio.wait_for(asyncio.to_thread(saver.save_sql_db, sql_tuples), timeout=600.0)
            print("SQL сохранён успешно")
        except Exception as e:
            print(f"Ошибка сохранения SQL: {e}")

        print("Готово!")
    finally:
        await fetcher.close()

if __name__ == '__main__':
    asyncio.run(main())