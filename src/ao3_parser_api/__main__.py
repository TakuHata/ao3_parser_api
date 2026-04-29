#from ao3_parser_api.fetcher import AO3fetcher
from ao3_parser_api.parser import AO3parser

def main():
    print('Running AO3 Parser API...')
    parser = AO3parser()

    with open("C:\\Users\\Takumi\\Documents\\FFN API\\ao3_parser_api\\example.html", "r", encoding="utf-8") as f:
        file = f.read()

    sql_db = parser.get_works(file, 1)
    json_db = parser.get_works(file, 2)

if __name__ == '__main__':
    main()