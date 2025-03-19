from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, URLField
from wtforms.validators import DataRequired, Length, Email, URL, Optional

# ... existing forms ...

class EditProfileForm(FlaskForm):
    """
    Form for editing user profile information.
    
    Fields:
        username: User's display name
        email: User's email address
        bio: User's biography or description
        avatar: Profile picture upload field
        location: User's location
        website: User's personal website
        newsletter_subscription: Newsletter opt-in
    """
    username = StringField('Username', 
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', 
                       validators=[Optional(), Length(max=500)])
    avatar = FileField('Update Profile Picture', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    location = StringField('Location', 
                         validators=[Optional(), Length(max=100)])
    website = URLField('Website', 
                      validators=[Optional(), URL()])
    newsletter_subscription = BooleanField('Subscribe to Newsletter') 