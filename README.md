# Python Console Movie Search App (Sakila Database)

## Project Description

This project is an interactive **console-based Python application** for searching movies in the **Sakila MySQL database**.

The application allows users to search films using various criteria and provides paginated results (10 movies per page).  
Additionally, the project includes logging and analytics functionality using MongoDB to store and analyze user search activity.


## Features

- Search movies by:
  - Keyword in title
  - Keyword in description
  - Genre
  - Release year
  - Year range
  - Actor or actress name
- Pagination (10 movies per page with navigation)
- Search statistics:
  - Last 5 searches
  - 5 Most popular searches
  - Search parameters analysis
- Interactive text-based menu
- Logging of search queries to MongoDB


## Project Structure

Python_Project/
│
├── main_menu.py       # Application entry point
├── search.py          # Search logic
├── formatter.py       # Output formatting
├── log_writer.py      # Logging search queries
├── log_reader.py      # Reading search statistics
│
├── config.example.py  # Configuration template
├── .gitignore
└── README.md


## Configuration

Sensitive data (database credentials) is **not stored in the repository**.

To run the project locally:

1. Copy `config.example.py`
2. Rename it to `config.py`
3. Fill in your own credentials:
   - MySQL connection (Sakila database)
   - MongoDB connection (for logging)

Example:
```python
MYSQL_CONFIG = {
    'host': 'your_mysql_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'sakila'
}
```


##  How to Run

The application can be launched from any Python environment (IDE, terminal, or Jupyter Notebook).

from main_menu import main_menu
main_menu()

After launching the application, an interactive console menu appears where the user can choose search options.
    

## Technologies Used

- Python
- MySQL (Sakila database)
- MongoDB
- SQL
- Jupyter Notebook
- Console-based UI

## Purpose of the Project

This project was created as a final educational project to demonstrate:

Python modular architecture
Database integration (SQL + NoSQL)
Logging and analytics
Clean code structure
Secure handling of configuration data


## Author
Alla Lugovska