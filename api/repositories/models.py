from app import login_manager
from repositories.db import Database
from flask_login import UserMixin
from flask import current_app
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import jwt
import time
import base64


@dataclass
class RadType:
    Id: Optional[int] = None
    RADTypeId: Optional[str] = None
    RADType: Optional[str] = None


@dataclass
class Rad:
    Id: Optional[int] = None
    RADTypeId: Optional[str] = None
    RADId: Optional[str] = None
    RAD: Optional[str] = None
    radType: Optional[RadType] = None


@dataclass
class Account:
    Id: Optional[int] = None
    ParentAccountNo: Optional[str] = None
    AccountNo: Optional[str] = None
    ChartId: Optional[int] = None
    Account: Optional[str] = None
    AccountType: Optional[str] = None
    DR_CR: Optional[str] = None
    PostingLevel: Optional[str] = None
    InterCompanyFlag: Optional[str] = None
    SecurityStatus: Optional[str] = None
    Revaluation: Optional[str] = None
    Reconciliation: Optional[str] = None
    AccountControlClass: Optional[str] = None
    ClassDescription: Optional[str] = None
    ConversionTypeId: Optional[str] = None
    ConversionTypeDescription: Optional[str] = None
    UDF1: Optional[str] = None
    XBRLTag: Optional[str] = None
    UserCreated: Optional[str] = None
    DateCreated: Optional[str] = None


@dataclass
class ProposedBudget:
    Id: Optional[int] = None
    FiscalYear: Optional[str] = None
    BusinessUnitId: Optional[str] = None
    AccountNo: Optional[str] = None
    RAD: Optional[str] = None
    ProposedBudget: Optional[float] = None
    BusinessCaseName: Optional[str] = None
    BusinessCaseAmount: Optional[float] = None
    TotalBudget: Optional[float] = None
    Comments: Optional[str] = None
    businessUnit: Optional["BusinessUnit"] = None
    account: Optional[Account] = None


@dataclass
class BusinessUnit:
    Id: Optional[int] = None
    BusinessUnitId: Optional[str] = None
    BusinessUnit: Optional[str] = None
    CompanyId: Optional[str] = None
    Company: Optional[str] = None
    DateCreated: Optional[datetime] = None


@login_manager.user_loader
def load_user(user_id):
    user_data = Database().read(
        sql='SELECT * FROM "user" WHERE id = %s;', params=(user_id,)
    )
    user = User(**user_data)

    if user:
        return user
    return None


@dataclass
class User(UserMixin):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    image_file: Optional[bytes] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_created: Optional[datetime] = None
    is_root_user: bool = False
    user_creator_id: Optional[int] = None

    def __post_init__(self):
        """Convert binary image to base64 string if image_file is in binary format."""
        if isinstance(self.image_file, bytes):
            # Convert binary image data to a base64 encoded string
            self.image_file = base64.b64encode(self.image_file).decode("utf-8")

        if isinstance(self.is_root_user, int):
            self.is_root_user = bool(self.is_root_user)

    # Implement the method required by Flask-Login to get the user ID
    def get_id(self):
        return str(self.id) if self.id else None

    def get_reset_token(self, expires_sec=1800):
        payload = {
            "user_id": self.id,
            "exp": time.time() + expires_sec,
        }
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        return token

    @staticmethod
    def verify_reset_token(token):
        decoded_data = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        user_id = decoded_data.get("user_id")

        if user_id is None:
            return None

        user = Database().read(
            sql='SELECT * FROM "user" WHERE id = %s LIMIT 1',
            params=(user_id,),
        )
        return user


@dataclass
class UserRegistration:
    username: str = None
    email: str = None
    password: str = None
    confirm_password: str = None
    first_name: str = None
    last_name: str = None
    is_root_user: bool = False
    user_creator_id: int = None

    def validate(self):
        # Check if email is already taken
        result = Database().read(
            sql='SELECT * FROM "user" WHERE email = %s LIMIT 1;',
            params=(self.email,),
        )
        if result:
            raise ValueError("Email already taken!")

        # Check if username is already taken
        result = Database().read(
            sql='SELECT * FROM "user" WHERE username = %s LIMIT 1;',
            params=(self.username,),
        )
        if result:
            raise ValueError("Username already taken!")

        # Check if passwords match
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match!")


@dataclass
class UserBusinessUnit:
    Id: Optional[int] = None
    BusinessUnitId: Optional[int] = None
    UserId: Optional[int] = None
    businessUnit: Optional[BusinessUnit] = None
    user: Optional[User] = None


@dataclass
class BudgetEntryAdminView:
    Id: Optional[int] = None
    DisplayOrder: Optional[int] = None
    AccountNo: Optional[str] = None
    Account: Optional[str] = None
    RAD: Optional[str] = None
    ForecastMultiplier: Optional[float] = None
    ForecastComments: Optional[str] = None
