from typing import Union, Any, overload, Literal
from bs4 import BeautifulSoup
from .datatype import FicData

class AO3parser:
    @overload
    def get_works(self, html_page: str, output_format: Literal[1]) -> list[tuple[str, ...]]: ...

    @overload
    def get_works(self, html_page: str, output_format: Literal[2]) -> list[FicData]: ...

    def get_works(self, html_page: str, output_format: int = 1) -> Union[list[tuple[str, ...]], list[FicData]]:
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

            current, total =  self._parse_chapters(chapters_text)

            work_data: FicData = {
                "title": title_text,
                "author": author_text,
                "fandom": fandom_text,
                "datetime": datetime_text,
                "tags": tags_text,
                "summary": summary_text,
                "language": language_text,
                "words": self._clean_int(words_text),
                "chapters_current": current,
                "chapters_total": total,
                "comments": self._clean_int(comments_text),
                "kudos": self._clean_int(kudos_text),
                "hits": self._clean_int(hits_text),
                "url": url_text
            }
            data_for_db.append(work_data)
        
        if output_format == 1:
            return [tuple(d.values()) for d in data_for_db]
        elif output_format == 2:
            return data_for_db
        
        return []
    
    def _clean_int(self, text: str) -> int:
        if not text or text == "-":
            return 0
        clean_val = text.replace(",","").strip()
        return int(clean_val) if clean_val.isdigit() else 0
    
    def _parse_chapters(self, chapters_text: str) -> tuple[int, int | None]:
        parts = chapters_text.split("/")
        current = self._clean_int(parts[0])

        total_raw = parts[1] if len(parts) > 1 else ""
        total = self._clean_int(total_raw) if total_raw != "?" else None

        return current, total


