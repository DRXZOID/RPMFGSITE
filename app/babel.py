from flask import request, session
from flask_babel import Babel

babel = Babel()

@babel.localeselector
def get_locale():
    # Try to get language from session
    if 'language' in session:
        return session['language']
    
    # Try to get language from browser
    return request.accept_languages.best_match(['en', 'ua', 'ru']) 