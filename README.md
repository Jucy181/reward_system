# Reward System Web App 

A Django-based web application that has two main components:

1. **Admin Facing:** Allows admins to manage Android apps and assign points to users.  
2. **User Facing:** Enables users to sign up, complete tasks such as downloading apps, and upload screenshots as proof to earn points.  

All features are also available via REST APIs with proper authentication, permissions, and documentation.

---

## Project Overview / Features

### Admin Panel (Custom, not Django Admin)
- Add Android apps and assign points for downloading apps
- View and manage users and their points
- Track completed tasks

### User Panel
- Signup and login (with authentication)
- View profile and points earned
- See tasks assigned by admin
- Upload screenshots to verify task completion (drag-and-drop supported)

### REST API
- All features available via API endpoints
- Authentication and permissions for secure access
- API documentation included

---

## Installation & Setup
1. **Clone the repository**

```bash
git clone https://gitlab.com/your-username/reward_system.git
cd reward_system

2.**Create a virtual environment**

python -m venv venv


3.**Activate the virtual environment**

# Windows:

venv\Scripts\activate

# macOS/Linux:

source venv/bin/activate

4.**Install dependencies**

pip install -r requirements.txt


5.**Run migrations and start the server**

python manage.py migrate
python manage.py runserver


6.**Open your browser** at http://localhost:8000

| Endpoint                 | Method | Description                  |
| ------------------------ | ------ | ---------------------------- |
| /api/users/register/     | POST   | Register a new user          |
| /api/users/login/        | POST   | User login                   |
| /api/tasks/              | GET    | List all tasks               |
| /api/screenshots/upload/ | POST   | Upload screenshot for a task |
| /api/points/             | GET    | View user points             |

## Contributing

Fork the repository and create a new branch for your feature/fix

Make your changes and commit with a descriptive message

Open a merge request for review

## Author

Jucy Abraham
 GitLab: https://gitlab.com/Jucy97

## License

MIT License © 2025 Jucy Abraham


## Deployment 

The Reward System was deployed on **Render** (https://my-first-project-2-wvkv.onrender.com).  

### Steps for Deployment:

1. Push code to GitLab.
2. Connect Render to GitLab repository.
3. Choose **Manual Deploy → Deploy latest commit**.
4. Render installs dependencies and runs the project with Gunicorn.
5. The live app is available at: https://my-first-project-2-wvkv.onrender.com

**Notes:**
- Free instances may spin down with inactivity, causing slow initial requests.
- Paid plans recommended for production stability.

### Problem Set I – Regex

Solution available in [`regex_solution.py`](regex_solution.py)


## Problem 3:

### A. Scheduling Periodic Tasks

I chose **Celery with Django** to schedule periodic tasks (like downloading ISINs every 24 hours) because it supports cron-like scheduling, retries, and asynchronous execution.

**Reliability & scalability:** Works well with Redis/RabbitMQ and can scale with multiple workers.
**Limitations: Managing many workers and brokers can be complex.
**Alternative at scale: Use AWS Lambda / Google Cloud Tasks or Kubernetes auto-scaling.

### B. Flask vs Django

**Flask:** Lightweight, flexible, good for small projects or microservices.
**Django:** Full-featured, structured, ideal for large apps with built-in auth, admin, and ORM.