from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateTimeField,
    HiddenField,
    FieldList,
    FormField,
    BooleanField,
)
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app import db
from repositories.models import MasterEmail


class UserBusinessUnit(FlaskForm):
    id = HiddenField()
    user_id = HiddenField()
    is_business_unit_selected = BooleanField(default=False)
    business_unit = StringField()
    business_unit_id = StringField()

class UserBusinessUnits(FlaskForm):
    email = StringField("Email")
    date_created = DateTimeField(
        "Date Created", format="%Y-%m-%d %H:%M:%S", default=db.func.current_timestamp()
    )
    user_business_units = FieldList(
        FormField(UserBusinessUnit),
        min_entries=1,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")
    
    def validate_user_business_units(self, field):
        # Check if at least one business unit is selected
        if not any(unit.is_business_unit_selected.data for unit in self.user_business_units):
            raise ValidationError("At least one business unit must be selected")

class MasterEmailForm(FlaskForm):
    id = HiddenField()
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    date_created = DateTimeField(
        "Date Created", format="%Y-%m-%d %H:%M:%S", default=db.func.current_timestamp()
    )
    user_business_units = FieldList(
        FormField(UserBusinessUnit),
        min_entries=1,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")

    def validate_email(self, field):
        # Check if the email already exists in the User table
        existing_user = MasterEmail.query.filter_by(email=field.data).first()
        if existing_user:
            raise ValidationError("Email already exists, please use a different email")

    def validate_user_business_units(self, field):
        # Check if at least one business unit is selected
        if not any(unit.is_business_unit_selected.data for unit in self.user_business_units):
            raise ValidationError("At least one business unit must be selected")
