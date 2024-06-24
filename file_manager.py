import os
import re
from query_validator import fix_and_validate_query, extract_table_name

def read_query_from_file(filename):
  """
  This function reads the SQL query content from a specified file.
  """
  try:
    with open(filename, 'r') as file:
      queries = file.read().strip().split(';\n')
      queries = [query + ';' if i < len(queries) - 1 else query for i, query in enumerate(queries)]
      #queries = [query for query in queries if query.strip()]
    return queries
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return None
  
def search_query_in_directory(query, directory):
    """
    Search for a query in all .sql files in the specified directory.
    """
    try:

        
        # List all .sql files in the directory
        sql_files = [f for f in os.listdir(directory) if f.endswith('.sql')]
        
        found = False
        
        # Search through each file
        for file_name in sql_files:
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                file_content = file.read()
                query = query.strip()
                header_pattern = query.split('\n')[0].strip().split(':')[1].strip()
                if re.search(header_pattern, file_content):
                    #print(f"Query name '{query}' found in file: {file_name}")
                    existing_file = file_name
                    found = True
                    break
        
        
        if found:
            
            pattern = r'-- name: {}\s*:.*?;'.format(re.escape(header_pattern))
            match = re.search(pattern, file_content, re.DOTALL | re.IGNORECASE)
            if not match:
                print(f"Error: Could not find query section for '{query}' in file '{file_path}'.")
                return False
            
            start, end = match.span()
            new_file_content = file_content[:start] + query.strip() + file_content[end:]
            with open(file_path, 'w') as file:
                file.write(new_file_content)
    
            print(f"Query '{query}' replaced successfully in file '{file_path}'.")
            return file_path

        else:
            print(f"Query Not found, proceeding to append to file.")
            
            # Extract table name from the query
            table_name = extract_table_name(query)
            if not table_name:
                print("Error: Unable to extract table name from query.")
                return False

            # Construct file path
            file_path = os.path.join(directory, f"{table_name}.sql")

            # Append query to the file
            with open(file_path, 'a+') as file:
                file.write('\n\n' + query.strip() + '\n\n')

            print(f"Query appended to file '{table_name}.sql' successfully.")
            return True
    
    except Exception as e:
        print(f"Error searching query in directory: {e}")
        return False


def append_to_table_file(query, directory):
    """
    Appends the query to a file named after the last FROM table in the SQL query.
    Creates the file if it doesn't exist.
    """
    try:
        found = search_query_in_directory(query, directory)
        if found == True:
            print(f"Query Not found, proceeding to append to file.")
            # Extract table name from the query
            table_name = extract_table_name(query)
            if not table_name:
                print("Error: Unable to extract table name from query.")
                return False
            
            # Construct file path
            file_path = os.path.join(directory, f"{table_name}.sql")
            
            # Append query to the file
            with open(file_path, 'a+') as file:
                file.write(query.strip() + '\n\n')
            
            print(f"Query appended to file '{table_name}.sql' successfully.")
        elif found == False:
            print(f"Query found, don't replace")
            
        else:
             print(f"Query found in file '{found}'.")
             #not implemented yet.........................
    
    except Exception as e:
        print(f"Error appending query to table file: {e}")
        return False

    """
    Appends the query to a file named after the last FROM table in the SQL query.
    Creates the file if it doesn't exist.
    """
    try:
        found = search_query_in_directory(query, directory)
        if found == True:
            print(f"Query Not found, proceeding to append to file.")
        elif found == False:
            print(f"Query found, don't replace")
            return True
        else:
            print(f"Query found in file '{found}'.")
            return False

        # Extract table name from the query
        table_name = extract_table_name(query)
        if not table_name:
            print("Error: Unable to extract table name from query.")
            return False

        # Construct file path
        file_path = os.path.join(directory, f"{table_name}.sql")

        # Append query to the file
        with open(file_path, 'a+') as file:
            file.write(query.strip() + '\n\n')

        print(f"Query appended to file '{table_name}.sql' successfully.")
        return True

    except Exception as e:
        print(f"Error appending query to table file: {e}")
        return False