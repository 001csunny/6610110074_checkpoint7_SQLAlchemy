from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from wtforms import Field, widgets
from models import db
import models
from wtforms import StringField
from wtforms.validators import DataRequired


class TagListField(Field):
    widget = widgets.TextInput()

    def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.data = []

    def process_formdata(self, valuelist):
        data = []
        if valuelist:
            data = [x.strip() for x in valuelist[0].split(",")]

        if not self.remove_duplicates:
            self.data = data
            return

        self.data = []
        for d in data:
            if d not in self.data:
                self.data.append(d)

    def _value(self):
        if self.data:
            return ", ".join([t.name if isinstance(t, models.Tag) else t for t in self.data])
        else:
            return ""


BaseNoteForm = model_form(
    models.Note, base_class=FlaskForm, exclude=["created_date", "updated_date"],db_session=db.session
)


class NoteForm(BaseNoteForm):
    tags = TagListField("Tag")
    
class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])