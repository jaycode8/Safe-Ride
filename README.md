# SafeRide Project Setup Guide

## Prerequisites

Ensure you have the following installed on your system:
- Python (>= 3.8)
- MySQL Server
- Git

## 1. Clone the Repository

```sh
git clone https://github.com/jaycode8/Safe-Ride.git
cd Safe-Ride
```

## 2. Create and Activate a Virtual Environment

### On macOS/Linux:
```sh
python -m venv venv
source venv/bin/activate
```

### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```sh
pip install -r requirements.txt
```

## 4. Set Up MySQL Database

Log into MySQL and create the database:
```sh
mysql -u root -p
```

Then, run the following SQL command:
```sql
CREATE DATABASE <db_name>;
```

## 5. Update Database Configuration

Open `app/config.py` (or your specific settings file) and update the database settings:

```python
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "***")
DB_NAME: str = os.getenv("DB_NAME", "<db_name>")
```
Replace `DB_USER` and `DB_PASSWORD` with your MySQL credentials and the created `db_name`.

## 6. Start the Application

Run the App application using:
```sh
python -m app.main
```

The App should now be running! Access the documentation at:
```
http://127.0.0.1:8000/
```

## 🎉 Congratulations! Your SafeRide project is up and running.

