# Bulletin Board System

A modern, Flask-based bulletin board system with role-based permissions, multi-language support, and a responsive design.

## Features

### Core Features
- User registration and authentication
- Role-based authorization system
- Multi-language support (EN, ES, FR, DE, RU, ZH)
- Post creation and management
- Comment system
- Category organization
- Image upload support
- Responsive design

### User Features
- User profiles with avatars
- Activity tracking
- Permission-based access
- Comment management
- Post creation and editing

### Admin Features
- User management dashboard
- Role and permission management
- Category management
- Activity monitoring
- Content moderation

## Technology Stack

### Backend
- Python 3.8+
- Flask 2.2.5
- SQLAlchemy 1.4.41
- Flask-Login 0.6.2
- Flask-Babel 3.1.0

### Database Support
- SQLite (default)
- MySQL 8.0+
- PostgreSQL 13+

### Frontend
- HTML5
- CSS3
- JavaScript
- Font Awesome 5.15.4

## Installation

### Local Development

1. Clone the repository:
bash
git clone https://github.com/DRXZOID/RPMFGSITE
cd RPMFGSITE

2. Create and activate virtual environment:
bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
bash
pip install -r requirements.txt

4. Configure environment variables:
bash
cp .env.example .env

Edit .env with your configuration

5. Initialize the database:
bash
flask db init
flask db migrate
flask db upgrade

6. Run the development server:
bash
flask run


### Docker Deployment

1. Copy the environment file:
bash
cp .env.example .env


2. Build and start the containers:
bash
docker-compose up --build


3. Initialize the database:
bash
docker-compose exec app flask db init
docker-compose exec app flask db migrate
docker-compose exec app flask db upgrade

4. Create an admin user:
bash
docker-compose exec web flask create-admin



## Database Configuration

### SQLite (Default)

1. Create a SQLite database file:
bash
touch app/data-dev.db

2. Update the database URI in .env:
DATABASE_URI=sqlite:///app/data-dev.db


### MySQL

1. Create a MySQL database:
DB_TYPE=mysql
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bulletin


### PostgreSQL
DB_TYPE=postgresql
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bulletin


## Translation Management

### Extract Messages
bash
pybabel extract -F babel.cfg -o messages.pot .

### Update Translations
bash
pybabel update -i messages.pot -d app/translations

### Compile Translations
bash
pybabel compile -d app/translations


### Create New Language
bash
pybabel init -i messages.pot -d app/translations -l new_language


### Compile Translations

bash
pybabel compile -d app/translations

## Project Structure

bulletin-board/
├── app/
│ ├── init.py
│ ├── models.py
│ ├── babel.py
│ ├── routes/
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── auth.py
│ │ ├── main.py
│ │ └── profile.py
│ ├── static/
│ │ ├── style.css
│ │ └── uploads/
│ ├── templates/
│ │ ├── admin/
│ │ ├── auth/
│ │ ├── main/
│ │ └── base.html
│ └── translations/
├── migrations/
├── instance/
├── tests/
├── babel.cfg
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run.py


## User Roles and Permissions

### Roles
- Admin: Full system access
- Moderator: Content moderation
- Writer: Post creation and management
- User: Comments and basic interaction
- Guest: Read-only access

### Permission Levels
- READ (1)
- COMMENT (2)
- WRITE (4)
- MODERATE (8)
- ADMIN (16)

## Development


### Database Migrations
bash
flask db migrate -m "Migration message"
flask db upgrade


### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused

## Security Features
- Password hashing using Werkzeug
- CSRF protection
- Secure file uploads
- Permission-based access control
- Input validation and sanitization
- Docker security best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Authors
Project Link: https://github.com/DRXZOID/RPMFGSITE

## Acknowledgments

- Flask documentation and community
- SQLAlchemy documentation
- Bootstrap for design inspiration
- Font Awesome for icons