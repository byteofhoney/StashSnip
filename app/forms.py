from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

LANGUAGES = [
    ("python", "Python"),
    ("javascript", "JavaScript"),
    ("html", "HTML"),
    ("css", "CSS"),
    ("java", "Java"),
    ("cpp", "C++"),
    ("sql", "SQL"),
    ("bash", "Bash"),
    ("json", "JSON"),
    ("other", "Other"),
]

class SnippetForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    language = SelectField("Language", choices=LANGUAGES)
    code = TextAreaField("Code", validators=[DataRequired()])
    description = StringField("Description", validators=[Length(max=200)])
    tags = StringField("Tags (comma separated)")