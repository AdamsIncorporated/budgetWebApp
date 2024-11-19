from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask import current_app
import jwt
import base64


class RadType(db.Model):
    __tablename__ = "RadType"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True)
    RADTypeId = Column("RADTypeId", String, unique=True)
    RADType = Column("RADType", String, unique=True)


class Rad(db.Model):
    __tablename__ = "Rad"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    RADTypeId = Column("RADTypeId", String, ForeignKey("RadType.Id"))
    RADId = Column("RADId", String)
    RAD = Column("RAD", String)

    radType = relationship("RadType", backref="rads")


class Account(db.Model):
    __tablename__ = "Account"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True)
    ParentAccountNo = Column("ParentAccountNo", String)
    ChartId = Column("ChartId", Integer)
    AccountNo = Column("AccountNo", String, unique=True)
    Account = Column("Account", String)
    AccountType = Column("AccountType", String)
    DR_CR = Column("DR/CR", String)
    PostingLevel = Column("PostingLevel", String)
    InterCompanyFlag = Column("InterCompanyFlag", String)
    SecurityStatus = Column("SecurityStatus", String)
    Revaluation = Column("Revaluation", String)
    Reconciliation = Column("Reconciliation", String)
    AccountControlClass = Column("AccountControlClass", String)
    ClassDescription = Column("ClassDescription", String)
    ConversionTypeId = Column("ConversionTypeId", String)
    ConversionTypeDescription = Column("ConversionTypeDescription", String)
    UDF1 = Column("UDF1", String)
    XBRLTag = Column("XBRLTag", String)
    UserCreated = Column("UserCreated", String)
    DateCreated = Column("DateCreated", String)


class ProposedBudget(db.Model):
    __tablename__ = "ProposedBudget"

    Id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    FiscalYear = Column("FiscalYear", String)
    BusinessUnitId = Column(
        "BusinessUnitId", String, ForeignKey("BusinessUnit.BusinessUnitId")
    )
    AccountNo = Column("AccountNo", String, ForeignKey("Account.AccountNo"))
    RAD = Column("RAD", String)
    ProposedBudget = Column("ProposedBudget", Float)
    BusinessCaseName = Column("BusinessCaseName", String)
    BusinessCaseAmount = Column("BusinessCaseAmount", Float)
    TotalBudget = Column("TotalBudget", Float)
    Comments = Column("Comments", String)

    # Relationships
    businessUnit = relationship("BusinessUnit", backref="proposed_budgets")
    account = relationship("Account", backref="proposed_budgets")


class BusinessUnit(db.Model):
    __tablename__ = "BusinessUnit"

    Id = db.Column("Id", db.Integer, primary_key=True)
    BusinessUnitId = db.Column("BusinessUnitId", db.Text, nullable=True)
    BusinessUnit = db.Column("BusinessUnit", db.Text, nullable=True)
    CompanyId = db.Column("CompanyId", db.Text, nullable=True)
    Company = db.Column("Company", db.Text, nullable=True)
    DateCreated = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "User"

    Id = db.Column("Id", db.Integer, primary_key=True)
    Username = db.Column("Username", db.String(20), unique=True, nullable=False)
    Email = db.Column("Email", db.String(120), unique=True, nullable=False)
    Password = db.Column("Password", db.String(60), nullable=False)
    ImageFile = db.Column("ImageFile", db.LargeBinary, nullable=True)
    FirstName = db.Column("FirstName", db.String(20), nullable=False)
    LastName = db.Column("LastName", db.String(20), nullable=False)
    DateCreated = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )
    IsRootUser = db.Column("IsRootUser", db.Integer, nullable=False, default=0)
    UserCreatorId = db.Column("UserCreatorId", db.Integer, nullable=True, default=None)

    def to_dict(self):
        def encode_field(field_value):
            if isinstance(field_value, bytes):
                return base64.b64encode(field_value).decode("utf-8")
            return field_value

        # Loop over all columns and convert them to a dictionary
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = encode_field(value)

        return result

    @property
    def formattedDateCreated(self):
        if self.DateCreated:
            return self.DateCreated.strftime("%B %d, %Y")
        return None

    def get_reset_token(self, expires_sec=1800):
        # Create a payload with the user ID and expiration time
        payload = {
            "user_id": self.Id,
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


class UserBusinessUnit(db.Model):
    __tablename__ = "User_BusinessUnit"

    Id = db.Column("Id", db.Integer, primary_key=True)
    BusinessUnitId = db.Column(
        "BusinessUnitId",
        db.Integer,
        db.ForeignKey("BusinessUnit.BusinessUnitId"),
        nullable=False,
    )
    UserId = db.Column("UserId", db.Integer, db.ForeignKey("User.Id"), nullable=False)
    businessUnit = db.relationship("BusinessUnit", backref="user_business_units")
    user = db.relationship("User", backref="user_business_units")


class BudgetEntryAdminView(db.Model):
    __tablename__ = "BudgetEntryAdminView"
    Id = Column(
        "Id", Integer, primary_key=True, autoincrement=True, unique=True, nullable=False
    )
    DisplayOrder = Column("DisplayOrder", Integer, unique=True, nullable=False)
    AccountNo = Column("AccountNo", Text, ForeignKey("Account.AccountNo"))
    Account = Column("Account", Text, ForeignKey("Account.Account"))
    RAD = Column("RAD", Text, ForeignKey("Rad.RAD"))
    ForecastMultiplier = Column("ForecastMultiplier", Float)
    ForecastComments = Column("ForecastComments", Text)
