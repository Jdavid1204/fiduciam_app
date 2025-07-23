# Quote Scraper Dashboard

A Django web application that scrapes quotes from [quotes.toscrape.com](https://quotes.toscrape.com), stores them in a PostgreSQL database, and provides a clean dashboard for managing and filtering quotes.

## 🚀 Features

- **Web Scraping**: Automatically scrapes quotes, authors, and tags from multiple pages
- **Database Storage**: Efficient PostgreSQL storage with proper relationships
- **Dynamic Filtering**: Filter quotes by author or tag with real-time dropdowns
- **CSV Export**: Download all quotes in CSV format ( "Delete All Quotes" button included for testing purposes and quick database reset during development.)
- **Bulk Operations**: Delete all quotes with confirmation modal
- **Responsive UI**: Clean Bootstrap-based interface with dynamic updates
    

## 📋 Prerequisites

- Python 3.9.10
- PostgreSQL 12+
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/jdavid1204/fiduciam_app.git
cd fiduciam_app
```

### 2. Create Virtual Environment

```bash
conda create -n fiduciam python=3.9.10 -c conda-forge
conda activate fiduciam
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create PostgreSQL database:

```bash
psql postgres
CREATE DATABASE fiduciam_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fiduciam_db TO your_username;
\q
```

### 5. Environment Configuration

Create a `.env` file in `quotes_project/`:

```bash
# quotes_project/.env
SECRET_KEY=your-secret-key-here
DATABASE_NAME=fiduciam_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Django Setup

```bash
cd quotes_project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`
    

## 🏃‍♂️ Usage

1. **Scrape Quotes**: Click "Get Quotes" to scrape new quotes from the website
2. **Filter by Author**: Select an author from the dropdown and click "Show"
3. **Filter by Tag**: Select a tag from the dropdown and click "Show"
4. **Export Data**: Download all quotes as CSV file
5. **Delete All**: Remove all quotes, authors, and tags with confirmation

## 🏗️ Project Structure

```
fiduciam_app/
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies  
├── README.md                   # This file
└── quotes_project/             # Django project
    ├── .env                    # Environment variables (not in git)
    ├── manage.py               # Django management
    ├── quotes_app/             # Main application
    │   ├── migrations/         # Database migrations
    │   ├── services/           # Business logic
    │   │   └── scraper.py      # Web scraping
    │   ├── templates/          # HTML templates
    │   ├── models.py           # Database models
    │   ├── views.py            # Django views
    │   └── urls.py             # URL routing
    └── quotes_project/         # Project settings
        ├── settings.py         # Django configuration
        └── urls.py             # Main URL config
```

## ⚙️ Tech Stack

- **Python**: 3.9.10
- **Django**: 3.1.8
- **PostgreSQL**: Database
- **Selenium**: Web scraping
- **Bootstrap**: Frontend UI
