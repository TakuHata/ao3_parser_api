from typing import Union, Any, overload, Literal
from bs4 import BeautifulSoup

class AO3parser:
    @overload
    def get_works(self, html_page: str, output_format: Literal[1]) -> list[tuple[str, ...]]: ...

    @overload
    def get_works(self, html_page: str, output_format: Literal[2]) -> list[dict[str, Any]]: ...

    def get_works(self, html_page: str, output_format: int = 1) -> Union[list[tuple[str, ...]], list[dict[str, Any]]]:
        soup = BeautifulSoup(html_page, "lxml")

        works = soup.select("li.blurb")

        data_for_db: list[Any] = []

        for card in works:
            title_el = card.select_one('h4.heading a[href*="/works/"]')
            title_text = title_el.get_text(strip=True) if title_el else "Unknown Title"
            
            author_el = card.select_one('a[rel="author"]')
            author_text = author_el.get_text(strip=True) if author_el else "Anonymous"

            fandom_el = card.select_one("a.tag")
            fandom_text = fandom_el.get_text(strip=True) if fandom_el else "Unknown"

            datetime_el = card.select_one("p.datetime")
            datetime_text = datetime_el.get_text(strip=True) if datetime_el else "00.00.0000"

            tag_el = card.select("ul.tags li")

            if tag_el:
                tags_list = [t.get_text(strip=True) for t in tag_el]
                tags_text = ", ".join(tags_list)
            else:
                tags_text = "-"

            summary_el = card.select("blockquote.userstuff p")

            if summary_el:
                summary_list = [s.get_text(strip=True) for s in summary_el]
                summary_text = " ".join(summary_list)
            else:
                summary_text = "-"

            language_el = card.select_one("dd.language")
            language_text = language_el.get_text(strip=True) if language_el else "-"

            words_el = card.select_one("dd.words")
            words_text = words_el.get_text(strip=True) if words_el else "-"

            chapters_el = card.select_one("dd.chapters")
            chapters_text = chapters_el.get_text(strip=True) if chapters_el else "-"

            comments_el = card.select_one("dd.comments")
            comments_text = comments_el.get_text(strip=True) if comments_el else "-"

            kudos_el = card.select_one("dd.kudos")
            kudos_text = kudos_el.get_text(strip=True) if kudos_el else "-"

            hits_el = card.select_one("dd.hits")
            hits_text = hits_el.get_text(strip=True) if hits_el else "-"

            url_text = str(title_el.get('href')) if title_el else "-"

            work_data = {
                "title": title_text,
                "author": author_text,
                "fandom": fandom_text,
                "datetime": datetime_text,
                "tags": tags_text,
                "summary": summary_text,
                "language": language_text,
                "words": words_text,
                "chapters": chapters_text,
                "comments": comments_text,
                "kudos": kudos_text,
                "hits": hits_text,
                "url": url_text
            }
            data_for_db.append(work_data)
        
        if output_format == 1:
            return [tuple(d.values()) for d in data_for_db]
        elif output_format == 2:
            return data_for_db
        
        return []


