#from ao3_parser_api.fetcher import AO3fetcher
from ao3_parser_api.parser import AO3parser
from ao3_parser_api.saver import AO3saver

def main():
    print('Running AO3 Parser API...')
    parser = AO3parser()
    saver = AO3saver()

    with open("C:\\Users\\Takumi\\Documents\\FFN API\\ao3_parser_api\\example.html", "r", encoding="utf-8") as f:
        file = f.read()

    sql_db = parser.get_works(file, 1)
    json_db = parser.get_works(file, 2)

    saver.save_sql_db(sql_db)
    saver.save_json_db(json_db)

if __name__ == '__main__':
    main()