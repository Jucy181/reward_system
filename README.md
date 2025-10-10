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