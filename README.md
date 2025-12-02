# COMP3005-Project

**Video Demo**
- **Video Link:** 

## **How To Run**
- **Entry point:** `app/main.py` (starts the terminal UI and initialises the DB)

**Prerequisites**
- **Python:** Python 3.9+ installed and available on `PATH`.
- **PostgreSQL:** PostgreSQL server installed and running locally (or reachable remotely).
- **Tools:** `psql` command-line client (optional but helpful for DB setup).

**GitHub — Clone & Local Setup**
```powershell
https://github.com/AliShafik/COMP3005-Project.git
cd COMP30005-Project
```

**Quick Setup**
1. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Create the PostgreSQL database and user required by the default config in `app/main.py`.
	The application assumes the connection URL `postgresql://test:test@localhost:5432/project`.
	You can either create a matching DB/user, or edit the connection string inside `app/main.py`.

	Example `psql` commands (run as a PostgreSQL superuser, e.g. `postgres`):

```powershell
# Replace with your admin user if not 'postgres'
# Create user 'test' with password 'test'
psql -U postgres -c "CREATE USER test WITH PASSWORD 'test';"
# Create database 'project' owned by 'test'
psql -U postgres -c "CREATE DATABASE project OWNER test;"
# (Optional) grant privileges if needed
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE project TO test;"
```

3. (Optional) If you prefer to use a different DB user/name/password, open `app/main.py` and change the SQLAlchemy engine URL near the top of the file:

```python
# In app/main.py
engine = create_engine("postgresql://test:test@localhost:5432/project", echo=False)
```

4. Start the application (from project root):

```powershell
# Make sure the virtualenv is activated
python .\app\main.py
```

**Notes**:
- On first run `app/main.py` will reset the public schema and create the tables using SQLAlchemy models, then execute the SQL files in the `sql/` folder (`view.sql` and `trigger.sql`).
- If you already have data you want to keep, update `app/main.py` to avoid `reset_db` or back up the database first.

**Running & Usage**
- After starting `app/main.py` the app pre-populates sample data and opens a CLI.
- Use the CLI menus to log in as Members/Trainers/Admins and try the implemented operations (registration, scheduling, availability, room booking, billing simulation, etc.).

