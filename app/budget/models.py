from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db


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
