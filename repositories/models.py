from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db, login_manager
from app.auth.models import User
from datetime import datetime, timedelta
from flask_login import jwt
from flask import current_app


class Account(db.Model):
    __tablename__ = "Account"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    parent_account_no = Column("ParentAccountNo", String)
    chart_id = Column("ChartId", Integer)
    account_no = Column("AccountNo", String, unique=True)
    account = Column("Account", String)
    account_type = Column("AccountType", String)
    dr_cr = Column("DR/CR", String)
    posting_level = Column("PostingLevel", String)
    inter_company_flag = Column("InterCompanyFlag", String)
    security_status = Column("SecurityStatus", String)
    revaluation = Column("Revaluation", String)
    reconciliation = Column("Reconciliation", String)
    account_control_class = Column("AccountControlClass", String)
    class_description = Column("ClassDescription", String)
    conversion_type_id = Column("ConversionTypeId", String)
    conversion_type_description = Column("ConversionTypeDescription", String)
    udf1 = Column("UDF1", String)
    xbrl_tag = Column("XBRLTag", String)
    user_created = Column("UserCreated", String)
    date_created = Column("DateCreated", String)

    def __repr__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"<Account({attributes})>"


class ProposedBudget(db.Model):
    __tablename__ = "ProposedBudget"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    fiscal_year = Column("FiscalYear", String)
    business_unit_id = Column(
        "BusinessUnitId", String, ForeignKey("BusinessUnit.BusinessUnitId")
    )
    account_no = Column("AccountNo", String, ForeignKey("Account.AccountNo"))
    proposed_budget = Column("ProposedBudget", Float)
    business_case_name = Column("BusinessCaseName", String)
    business_case_amount = Column("BusinessCaseAmount", Float)
    comments = Column("Comments", String)
    total_budget = Column("TotalBudget", Float)

    # Relationships
    business_unit = relationship("BusinessUnit", backref="proposed_budgets")
    account = relationship("Account", backref="proposed_budgets")

    def __repr__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"<ProposedBudget({attributes})>"


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "User"

    id = db.Column("Id", db.Integer, primary_key=True)
    username = db.Column("Username", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    password = db.Column("Password", db.String(60), nullable=False)
    image_file = db.Column("ImageFile", db.LargeBinary, nullable=True)
    first_name = db.Column("FirstName", db.String(20), nullable=False)
    last_name = db.Column("LastName", db.String(20), nullable=False)
    date_created = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )
    is_root_user = db.Column("IsRootUser", db.Integer, nullable=False, default=0)

    def get_reset_token(self, expires_sec=1800):
        # Create a payload with the user ID and expiration time
        payload = {
            "user_id": self.id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_sec),
        }
        # Encode the payload using the secret key
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token):
        try:
            # Decode the token using the secret key
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user_id = payload["user_id"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        return User.query.get(user_id)
