MAIN_URL = "https://archiveofourown.org/works"
BASE_URL = "https://archiveofourown.org/works?work_search[sort_column]=revised_at&work_search[other_tag_names]=&work_search[excluded_tag_names]=&work_search[crossover]=F&work_search[complete]=&work_search[words_from]=&work_search[words_to]=&work_search[date_from]=&work_search[date_to]=&work_search[query]=&work_search[language_id]=en&exclude_work_search[category_ids][]=23&commit=Sort+and+Filter&tag_id=Naruto+%28Anime+*a*+Manga%29&page="
PAGES = 2595

USER_AGENT = "MyAO3SearchBot/1.0 (https://github.com/TakuHata; nameno6112@gmail.com)"

EXTRA_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8"
}

MAX_STREAMS = 5

CHUNK_SIZE = 50

URLS = [f"{BASE_URL}{i}" for i in range(1, PAGES)]