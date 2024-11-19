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
    Id: int
    RADTypeId: str
    RADType: str


@dataclass
class Rad:
    Id: int
    RADTypeId: str
    RADId: str
    RAD: str
    radType: Optional[RadType] = None


@dataclass
class Account:
    Id: int
    ParentAccountNo: Optional[str] = None
    ChartId: Optional[int] = None
    AccountNo: str
    Account: str
    AccountType: str
    DR_CR: str
    PostingLevel: str
    InterCompanyFlag: str
    SecurityStatus: str
    Revaluation: str
    Reconciliation: str
    AccountControlClass: str
    ClassDescription: str
    ConversionTypeId: str
    ConversionTypeDescription: str
    UDF1: str
    XBRLTag: str
    UserCreated: str
    DateCreated: str


@dataclass
class ProposedBudget:
    Id: int
    FiscalYear: str
    BusinessUnitId: str
    AccountNo: str
    RAD: str
    ProposedBudget: float
    BusinessCaseName: str
    BusinessCaseAmount: float
    TotalBudget: float
    Comments: str
    businessUnit: Optional["BusinessUnit"] = None
    account: Optional[Account] = None


@dataclass
class BusinessUnit:
    Id: int
    BusinessUnitId: Optional[str] = None
    BusinessUnit: Optional[str] = None
    CompanyId: Optional[str] = None
    Company: Optional[str] = None
    DateCreated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class User:
    Id: int
    Username: str
    Email: str
    Password: str
    ImageFile: Optional[bytes] = None
    FirstName: str
    LastName: str
    DateCreated: datetime = field(default_factory=datetime.utcnow)
    IsRootUser: int = 0
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
    Id: int
    BusinessUnitId: int
    UserId: int
    businessUnit: Optional[BusinessUnit] = None
    user: Optional[User] = None


@dataclass
class BudgetEntryAdminView:
    Id: int
    DisplayOrder: int
    AccountNo: str
    Account: str
    RAD: str
    ForecastMultiplier: Optional[float] = None
    ForecastComments: Optional[str] = None
