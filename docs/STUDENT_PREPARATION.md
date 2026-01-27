# Student Preparation Guide


Welcome to the **Django Store & Product API** workshop!
Before coming to the class, please complete the following setup steps to ensure we can start coding right away.


## 1. Install Required Software


### A. Python (Version 3.10 or higher)
*   **Download**: [python.org/downloads](https://www.python.org/downloads/)
*   **Verify**: Open your terminal (or command prompt) and run:
   ```bash
   python --version
   # On Mac/Linux, you might need to try: python3 --version
   # Ensure it says Python 3.10.x or higher
   ```


### B. Code Editor (VS Code Recommended)
*   **Download**: [code.visualstudio.com](https://code.visualstudio.com/)
*   **Extensions**: Install the **Python** extension by Microsoft from the Extensions view (`Ctrl+Shift+X`).


### C. Git
*   **Download**: [git-scm.com/downloads](https://git-scm.com/downloads)
*   **Verify**: Run `git --version` in terminal.










### D. ODBC Driver 18 for SQL Server 
This is needed for the database connector library (`pyodbc`) to install correctly.
*   **Windows**: [Download and Install]
(https://go.microsoft.com/fwlink/?linkid=2249006)
*   **macOS**:
   ```bash
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   brew update
   brew install msodbcsql18 mssql-tools18
   ```
*   **Linux (Ubuntu)**: [Installation Instructions]
(https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)


### E. MongoDB
We will use MongoDB for the Reviews feature.
*   **MongoDB Community Server**: [Download](https://www.mongodb.com/try/download/community)
   *   Install the MSI (Windows) or use Brew (Mac).
*   **MongoDB Compass** (GUI): [Download](https://www.mongodb.com/try/download/compass)


---


## 2. Project Setup


### A. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/raksit/azure_sql_django.git
cd azure_sql_django
```


### B. Create a Virtual Environment
This keeps our project dependencies isolated.
```bash
# Windows
python -m venv venv


# Mac/Linux
python3 -m venv venv
```


### C. Install Dependencies
```bash
# Windows
.\venv\Scripts\pip install -r requirements.txt


# Mac/Linux
./venv/bin/pip install -r requirements.txt
```


---


## 3. Verify Your Setup


Run the following command to make sure everything is installed correctly:
```bash
# Windows
.\venv\Scripts\python manage.py check


# Mac/Linux
./venv/bin/python manage.py check
```
If you see **"System check identified no issues"**, you are ready for the class!


See you there!





