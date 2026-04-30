import sqlite3
import json
from pathlib import Path
from .datatype import FicData

class AO3saver:
    current_file = Path(__file__).resolve()
    data_dir = current_file.parents[2] / "data"

    def save_sql_db(self, data: list[tuple[str, ...]]):
        with sqlite3.connect(f"{self.data_dir}/data/fics_db.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Fics
                (id INTEGER PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                fandom TEXT NOT NULL,
                datetime TEXT NOT NULL,
                tags TEXT NOT NULL,
                summary TEXT NOT NULL,
                language TEXT NOT NULL,
                words INTEGER NOT NULL,
                chapters_current INTEGER NOT NULL,
                chapters_total INTEGER,
                comments INTEGER NOT NULL,
                kudos INTEGER NOT NULL,
                hits INTEGER NOT NULL,
                url TEXT NOT NULL)
            ''')
            cursor.executemany('''
                INSERT INTO Fics (title, author, fandom, datetime, tags, summary, language, 
                words, chapters_current, chapters_total, comments, kudos, hits, url) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )''', data)
            connection.commit()
            print("Данные добавлены в таблицу sqlite3")

    def save_json_db(self, data: list[FicData]):
        with open(f"{self.data_dir}/data/fics_db.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные добавлены в json")
