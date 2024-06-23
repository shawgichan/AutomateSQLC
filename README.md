# AutomateSQLC

AutomateSQLC is a Python tool designed to automate SQL query management in large Go projects using sqlc. It streamlines the process of validating, adding, and updating SQL queries across multiple files.

## Features

- Validates SQL query structure
- Checks for existing queries and offers replacement
- Handles file management (appending to existing files or creating new ones)
- Works with large codebases (tested with 3500+ queries across 350+ files)

## Installation

You can install AutomateSQLC with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/AutomateSQLC/main/install.sh | bash
```

Alternatively, you can manually install:

1. Ensure you have Python 3.7+ installed on your system.
2. Navigate to your Go project's root directory.
3. Create a `scripts` folder if it doesn't already exist:
   mkdir -p scripts
4. Clone the AutomateSQLC repository into the`scripts` folder:
   git clone https://github.com/shawgichan/AutomateSQLC.git scripts/AutomateSQLC
5. Navigate to the AutomateSQLC directory:
   cd scripts/AutomateSQLC
6. Install the required dependencies:
   pip install -r requirements.txt

## Usage

1. Navigate to your project's root directory.
2. Place your SQL query in the `scripts/AutomateSQLC/input_query.sql` file .
3. Run the script:
   python scripts/AutomateSQLC/main.pypython main.py
   The script will validate the query, check if it already exists, and either update an existing query or append it to a new or existing file in the `db/query/` directory.

## File Structure

your_go_project/
├── db/
│   ├── query/
│   │   └── (SQL query files will be here)
│   └── sqlc/
│       └── (sqlc generated output)
├── scripts/
│   └── AutomateSQLC/
│       ├── __init__.py
│       ├── query_validator.py
│       ├── file_manager.py
│       ├── main.py
│       ├── input_query.sql
│       ├── requirements.txt
│       └── README.md
└── (other project files and folders)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Plans

- Support for processing multiple queries at once
- Automatic file cleanup after query addition
- Integration with sqlc generate command
- Extensive testing and code review

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Shawgi Hafiz - https://www.linkedin.com/in/shawgi-hafiz-a13a471bb/

Project Link: [https://github.com/shawgichan/AutomateSQLC.git](https://github.com/shawgichan/AutomateSQLC.git)
