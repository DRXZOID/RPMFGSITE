# Bulletin Board System

A modern, Flask-based bulletin board system with role-based permissions and a responsive design.

## Features

### User Management
- User registration and authentication
- Role-based authorization system
- User profiles with avatars
- Activity tracking

### Content Management
- Post creation and management
- Category organization
- Image upload support
- Comment system
- Rich text formatting

### Admin Features
- User management dashboard
- Role and permission management
- Category management
- Activity monitoring
- Content moderation

### Technical Features
- Responsive design
- Mobile-friendly interface
- Secure file uploads
- Flash messages for user feedback
- Permission-based UI elements

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.2.5
- **Database**: SQLite (SQLAlchemy)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **File Upload**: Werkzeug
- **CSS Framework**: Custom responsive design

## Dependencies

- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Mail
- Flask-Bcrypt
- Flask-Uploads
- Flask-Gravatar
- Flask-Limiter
- Flask-HTTPAuth
- Flask-RESTful
- Flask-JWT-Extended

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bulletin-board.git
cd bulletin-board
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the development server:
```bash
python run.py
```

## Project Structure

```
bulletin-board/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── profile.py
│   ├── static/
│   │   ├── style.css
│   │   └── uploads/
│   └── templates/
│       ├── admin/
│       ├── auth/
│       ├── main/
│       └── base.html
├── migrations/
├── instance/
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

## User Roles and Permissions

- **Admin**: Full system access
- **Moderator**: Content moderation
- **Writer**: Post creation and management
- **User**: Comments and basic interaction
- **Guest**: Read-only access

### Permission Levels

1. READ (1)
2. COMMENT (2)
3. WRITE (4)
4. MODERATE (8)
5. ADMIN (16)

## Development

### Running Tests
```bash
python -m pytest
```

### Database Migrations
```bash
flask db migrate -m "Migration message"
flask db upgrade
```

### Adding New Features
1. Create new routes in appropriate route file
2. Add templates in templates directory
3. Update models if needed
4. Add CSS styles in style.css
5. Run tests and verify functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security

- Password hashing using Werkzeug
- CSRF protection
- Secure file uploads
- Permission-based access control
- Input validation and sanitization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- SQLAlchemy documentation
- Frontend design inspiration from modern bulletin boards

## Contact

Project Link: https://github.com/DRXZOID/RPMFGSITE

