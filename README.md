# Account Expense Tracker

A full-featured Django web application for managing financial accounts and tracking transactions. This app allows users to register, create multiple accounts, and log inflows and expenses with receipt uploads for each transaction. 

Sign up and use it as deployed on Render: 🌐 https://account-tracker-django.onrender.com/

<img width="2906" height="1570" alt="image" src="https://github.com/user-attachments/assets/402668df-a40f-4bc2-95d1-ab559026189b" />

-----

## \#\# Key Features

  * **Secure User Authentication:** Users can register, log in, and manage their own private accounts.
  * **Multi-Account Management:** Create and manage several distinct financial accounts.
  * **Transaction Tracking:** Log inflows and expenses for each account with details like date, amount, and description.
  * **Receipt Uploads:** Attach a file (e.g., a receipt) to every transaction for better record-keeping.
  * **Dynamic Currency Support:** Choose a currency (BDT, USD, EUR, GBP, or Other) for each account, and the correct symbol will be displayed throughout the app.
  * **Responsive UI:** A clean, modern, and mobile-friendly interface built with Bootstrap 5.

-----

## \#\# Tech Stack

  * **Backend:** Django
  * **Frontend:** HTML, CSS, Bootstrap 5
  * **Database:** PostgreSQL (Production), SQLite3 (Development)
  * **Media File Storage:** Cloudinary
  * **Deployment:** Render
  * **WSGI Server:** Gunicorn

-----

## \#\# Getting Started (Local Setup)

Follow these instructions to get a copy of the project running on your local machine for development and testing. This guide uses a `.env` file to manage secret keys and other settings, which should never be committed to Git.

### \#\#\# Prerequisites

  * Python 3.8+
  * Git

### \#\#\# Installation & Setup

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and Activate a Virtual Environment**

      * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
      * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies**
    First, you need a small package to read the `.env` file.

    ```bash
    pip install python-dotenv
    pip install -r requirements.txt
    ```

4.  **Update `settings.py` to Load the `.env` File**
    Add the following two lines to the very top of your `account_log/settings.py` file. This will load your `.env` file automatically every time the application starts.

    ```python
    # At the top of account_log/settings.py
    from dotenv import load_dotenv
    load_dotenv()

    import os
    import dj_database_url
    from pathlib import Path
    # ... rest of the file
    ```

5.  **Create Your Local `.env` File**
    In the root of your project (the same folder as `manage.py`), create a file named `.env`. Copy and paste the following, replacing the placeholder values with your own keys.

    ```env
    # Django Settings
    # Generate a new secret key for development. Do not use the production key.
    SECRET_KEY='django-insecure-a-very-strong-local-secret-key'
    DEBUG='True'

    # Database URL (uses the local SQLite file by default)
    DATABASE_URL='sqlite:///db.sqlite3'

    # Your Cloudinary Credentials (get from your Cloudinary dashboard)
    CLOUDINARY_CLOUD_NAME='your_cloud_name'
    CLOUDINARY_API_KEY='your_api_key'
    CLOUDINARY_API_SECRET='your_api_secret'
    ```

6.  **IMPORTANT: Secure Your Secrets**
    Your `.env` file contains sensitive information. It must **never** be committed to GitHub. Create or open the `.gitignore` file in your project root and add `.env` to it.

    ```
    # .gitignore

    # Environment variables
    .env

    # Other files...
    db.sqlite3
    ```

7.  **Run Database Migrations**

    ```bash
    python manage.py migrate
    ```

8.  **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

    Your application will now be running at `http://127.0.0.1:8000`, configured with the settings from your `.env` file.
