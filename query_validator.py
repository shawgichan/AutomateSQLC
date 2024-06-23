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
        query = re.sub(r'\s*:\s*(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', 
                       lambda m: f" :{m.group(1).lower()}", query)

        # Find the '-- name: QueryName :attr' comment
        name_comment_match = re.search(r'-- name: (\w+) :(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', query)
        if not name_comment_match:
            comment_query = query.split('\n')[0].strip()
            print(f"Error: Missing or invalid '-- name: {comment_query.split(':')[1].strip()} :{comment_query.split(':')[2].strip()}' Wrong Header Format.")
            return False

        # Validate and fix the comment
        query_name, attr = name_comment_match.groups()
        query_name = query_name[0].upper() + query_name[1:]
        fixed_comment = f"-- name: {query_name} :{attr}"
        query = re.sub(r'-- name: \w+ :(exec|execresult|execrows|execlastid|many|one|batchexec|batchmany|batchone)', 
                       fixed_comment, query, count=1)

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
    Extracts the table name after the last FROM keyword in the SQL query.
    """
    parts = query.rsplit('FROM', 1)
    if len(parts) == 2:
        table_name = parts[1].split()[0].strip()
        table_name_without_semicolon = table_name[:-1] if table_name.endswith(';') else table_name
        return table_name_without_semicolon
    else:
        return None