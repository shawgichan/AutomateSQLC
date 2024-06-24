import os
from query_validator import fix_and_validate_query
from file_manager import read_query_from_file, append_to_table_file, search_query_in_directory

def main():
    queries = read_query_from_file(filename='db/input/query.sql')
    for index, query in enumerate(queries):
            print(search_query_in_directory(query, 'db/query'))

if __name__ == "__main__":
    main()