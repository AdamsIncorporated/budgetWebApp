from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateTimeField,
    SelectField,
    HiddenField
)
from wtforms.validators import DataRequired, Email, Length
from app import db
from repositories.models import BusinessUnit


class MasterEmailForm(FlaskForm):
    id = HiddenField()
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    business_unit_table_id = SelectField(
        "Business Unit",
        validators=[DataRequired()],
        coerce=int,
    )
    date_created = DateTimeField(
        "Date Created", format="%Y-%m-%d %H:%M:%S", default=db.func.current_timestamp()
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(MasterEmailForm, self).__init__(*args, **kwargs)
        business_units = (
            BusinessUnit.query.with_entities(
                BusinessUnit.id, BusinessUnit.business_unit
            )
            .distinct()
            .all()
        )
        self.business_unit_table_id.choices = [
            (bu.id, bu.business_unit) for bu in business_units
        ]