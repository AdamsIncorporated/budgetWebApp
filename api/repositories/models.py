from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
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
    IsRootUser: bool = False
    UserCreatorId: Optional[int] = None

    def __post_init__(self):
        """Convert binary image to base64 string if ImageFile is in binary format."""
        if isinstance(self.ImageFile, bytes):
            # Convert binary image data to a base64 encoded string
            self.ImageFile = base64.b64encode(self.ImageFile).decode("utf-8")

        if isinstance(self.IsRootUser, int):
            self.IsRootUser = bool(self.IsRootUser)


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
