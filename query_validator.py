import re
import sqlparse
from sqlparse.tokens import DML, Keyword

VALID_ATTRS = {
    "exec", "execresult", "execrows", "execlastid",
    "many", "one", "batchexec", "batchmany", "batchone"
}

def fix_and_validate_query(query):
    """
    Fix common mistakes in the SQL query and validate the format.
    """
    try:
        # Ensure the query starts with '-- name:'
        query = re.sub(r'--\s*name\s*:\s*', '-- name: ', query, flags=re.IGNORECASE, count=1)
        query = re.sub(r'\s*:\s*(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', lambda m: f" :{m.group(1).lower()}", query)
        #query = re.sub(r'--\s*name\s*:', '-- name:', query, count=1)
        
        # Find the '-- name: QueryName :attr' comment
        name_comment_match = re.search(r'-- name: (\w+) :(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', query)
        if not name_comment_match:
            comment_query = query.split('\n')[0].strip()
            print("Error: Missing or invalid '-- name: "+comment_query.split(':')[1].strip()+" :"+comment_query.split(':')[2].strip()+"' Wrong Header Format.")
            
            return False

        # Validate and fix the comment
        query_name, attr = name_comment_match.groups()
        query_name = query_name[0].upper() + query_name[1:]
        fixed_comment = f"-- name: {query_name} :{attr}"
        query = re.sub(r'-- name: \w+ :(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', fixed_comment, query, count=1)
        
        # Parse the query
        parsed = sqlparse.parse(query)
        
        # Check for any DML statement (SELECT, UPDATE, DELETE, INSERT, etc.)
        if not any(any(token.ttype == DML for token in statement.tokens) for statement in parsed):
            print("Error: Missing DML statement (SELECT, UPDATE, DELETE, INSERT, etc.)")
            return False
        if not query.strip().endswith(';'):
            print("Error: Missing semicolon (;) at the end of the query.")
            return False
        # Print fixed query
        print(f"Fixed query: \n{query}\n\n")
        verified_query = sqlparse.format(query, reindent=True, keyword_case='upper') 
        print(f"Verified query: \n{verified_query}\n\n")
        # If all checks pass
        return True
    except Exception as e:
        print(f"Error parsing query: {e}")
        return False

def extract_table_name(query):
  """
  Extracts the table name after relevant keywords (FROM, INTO, UPDATE, DELETE) in the SQL query.
  """
  query = remove_name_comment_and_leading_newlines(query)
  query = query.strip().upper()  # Convert query to uppercase for case-insensitive matching
  if query.upper().startswith("WITH"):
      return 'common'
  if query.upper().startswith("UPDATE"):
      parts = query.split('UPDATE', 1)  # Split at the first occurrence of UPDATE
      if len(parts) == 2:
        table_name = parts[1].split()[0].strip()
        # Handle trailing characters (semicolon, whitespace) or parentheses
        if table_name and table_name[-1] in (';', ' ', ')'):
          table_name = table_name[:-1]
        return table_name.lower()  # Convert to lowercase for case-insensitive matching
      
  if query.upper().startswith("SELECT"):
        parts = query.split('FROM', 1)
        if len(parts) == 2:
            table_name = parts[1].split()[0].strip()
        # Handle trailing characters (semicolon, whitespace) or parentheses
            if table_name and table_name[-1] in (';', ' ', ')', '('):
                table_name = table_name[:-1]
            return table_name.lower()  # Convert table name to lowercase for case-insensitive matching
  if query.upper().startswith("INSERT"):
        parts = query.split('INTO', 1)
        if len(parts) == 2:
            table_name = parts[1].split()[0].strip()
        # Handle trailing characters (semicolon, whitespace) or parentheses
            if table_name and table_name[-1] in (';', ' ', ')', '('):
                table_name = table_name[:-1]
            return table_name.lower()  # Convert table name to lowercase for case-insensitive matching
  if query.upper().startswith("DELETE"):
        parts = query.split('FROM', 1)
        if len(parts) == 2:
            table_name = parts[1].split()[0].strip()
        # Handle trailing characters (semicolon, whitespace) or parentheses
            if table_name and table_name[-1] in (';', ' ', ')', '('):
                table_name = table_name[:-1]
            return table_name.lower()  # Convert table name to lowercase for case-insensitive matching

  return None  # Handle non-DML statements or unsupported formats

def remove_name_comment_and_leading_newlines(query):
  """
  Removes the first line containing "-- name:" and any leading newlines from a string.

  Args:
      query (str): The input string.

  Returns:
      str: The string with the target line and leading newlines removed,
           or the original string if no match is found.
  """

  lines = query.splitlines(keepends=True)  # Split by lines, keeping line endings
  new_lines = []

  for line in lines:
    if not line.upper().startswith("-- NAME:"):  # Check for "-- name:" (case-insensitive)
      new_lines.append(line)

  return ''.join(new_lines)
