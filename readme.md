## 💬 Real-Time Group Chat System

### Project Overview

This is a **real-time group chat application** built using **Django Channels** for handling WebSocket connections. The frontend is developed with **Vue.js** and the **Vant UI** library, providing a smooth, mobile-friendly user experience. The application ensures instant message delivery through Channels and uses **MySQL** for robust data persistence.

### Key Features

  * **User Authentication**: Secure user registration and login functionality.
  * **Group Management**:
      * Create, edit, and delete chat groups.
      * View a list of available groups.
      * Join and leave groups.
  * **Real-Time Messaging**:
      * Instantaneous sending and receiving of messages within group chats.
      * Supports multiple concurrent users.
  * **Data Persistence**: All chat messages and group data are stored in a **MySQL** database, allowing for historical message retrieval.

### Tech Stack

| Category | Technology | Key Components / Libraries |
| :--- | :--- | :--- |
| **Backend** | **Python (Django)** | Django Channels (WebSocket), Django REST Framework (DRF) |
| **Database** | **MySQL** | `mysqlclient` |
| **Async / Caching** | **Redis** | Used as the Channel Layer Backend |
| **Frontend** | **Vue.js** | Vant UI (Mobile Component Library), Axios, native WebSocket API |

### Local Setup Guide

Before starting, ensure you have **Python 3.8+**, **Node.js (npm/yarn)**, **MySQL** server, and **Redis** server installed and running on your system.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/qianfu323/ChatFlow.git
cd ChatFlow
```

#### Step 2: Backend Setup (Django)

1.  **Create and Activate Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate.bat  # Windows
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Database Configuration (MySQL)**

      * Create a MySQL database (e.g., `chat_db`).

      * Update the `DATABASES` configuration in `backend/chat_project/settings.py` with your credentials:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'chat_db',  # Database name
                'USER': 'your_mysql_user',  # MySQL username
                'PASSWORD': 'your_mysql_password',  # MySQL password
                # ... other settings
            }
        }
        ```

4.  **Run Migrations**

    ```bash
    cd backend
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Start Backend Server (using Daphne)**

    ```bash
    # Run from the /backend directory
    python manage.py runserver 127.0.0.1:8000
    # Backend server should be running at http://127.0.0.1:8000
    ```

#### Step 3: Frontend Setup (Vue.js)

1.  **Install Dependencies**

    ```bash
    cd ../frontend  # Navigate to the frontend directory
    npm install
    # or yarn install
    ```

2.  **Configure API Endpoints**

      * Verify that the HTTP and WebSocket base URLs in the frontend code (e.g., in a configuration file or main script) correctly point to your backend (`ws://127.0.0.1:8000` and `http://127.0.0.1:8000`).

3.  **Start Frontend Server**

    ```bash
    npm run dev
    # Frontend server usually runs at http://127.0.0.1:5173
    ```

-----

## Instructions for Use

1.  **Access**: Open your browser to the frontend address (e.g., `http://127.0.0.1:5173`).
2.  **Auth**: Use the **Register** function to create a new user, then **Login**.
3.  **Create/Join**: Navigate to the Group List, where you can **Create a new Group** or **Join** an existing one.
4.  **Chat**: Enter a joined group. Messages sent will be delivered and displayed to all members in **real-time**. Historical messages are loaded from the database upon entry.

-----