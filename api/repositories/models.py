from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
import base64


def encode_field(field_value):
    if isinstance(field_value, bytes):
        return base64.b64encode(field_value).decode("utf-8")
    return field_value


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


@dataclass
class User:
    Id: Optional[int] = None
    Username: Optional[str] = None
    Email: Optional[str] = None
    Password: Optional[str] = None
    ImageFile: Optional[bytes] = None
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    DateCreated: Optional[datetime] = None
    IsRootUser: Optional[int] = None
    UserCreatorId: Optional[int] = None

    def to_dict(self):
        result = {
            field.name: encode_field(getattr(self, field.name))
            for field in self.__dataclass_fields__.values()
        }
        return result

    @property
    def formattedDateCreated(self):
        return self.DateCreated.strftime("%B %d, %Y") if self.DateCreated else None


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
