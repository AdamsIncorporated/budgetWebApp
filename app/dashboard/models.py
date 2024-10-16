from app import db, login_manager
from app.auth.models import User
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class BusinessUnit(db.Model):
    __tablename__ = "BusinessUnit"

    id = db.Column("Id", db.Integer, primary_key=True)
    business_unit_id = db.Column("BusinessUnitId", db.Text, nullable=True)
    business_unit = db.Column("BusinessUnit", db.Text, nullable=True)
    company_id = db.Column("CompanyId", db.Text, nullable=True)
    company = db.Column("Company", db.Text, nullable=True)
    date_created = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )


class MasterEmail(db.Model):
    __tablename__ = "MasterEmail"

    id = db.Column("Id", db.Integer, primary_key=True)
    email = db.Column("Email", db.Text, unique=True, nullable=False)
    user_creator_id = db.Column(
        "UserCreatorId", db.Integer, ForeignKey("User.Id"), nullable=False
    )
    business_unit_table_id = db.Column(
        "BusinessUnitTableId", db.Integer, ForeignKey("BusinessUnit.Id"), nullable=False
    )
    date_created = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )

    master_email_business_unit = db.relationship(
        "BusinessUnit", backref="master_emails"
    )

    master_email_user = db.relationship("User", backref="master_user")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
