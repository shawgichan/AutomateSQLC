import os
from query_validator import fix_and_validate_query
from file_manager import read_query_from_file, append_to_table_file

def main():
    # Set the paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'input_query.sql')
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'db', 'query')

    # Read the query from file
    query = read_query_from_file(input_file)
    if query is None:
        return

    # Validate and fix the query
    if not fix_and_validate_query(query):
        print("Query validation failed. Please check the error messages above.")
        return

    # Append the query to the appropriate file
    if append_to_table_file(query, output_dir):
        print("Query processing completed successfully.")
    else:
        print("Failed to process the query. Please check the error messages above.")

if __name__ == "__main__":
    main()