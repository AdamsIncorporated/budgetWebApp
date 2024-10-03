from app import db
from sqlalchemy import Column, Integer, Float, String, ForeignKey


class JournalEntry(db.Model):
    __tablename__ = "JournalEntry"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    company_id = Column("CompanyID", String, nullable=True)
    entry_id = Column("EntryId", String, nullable=True)
    business_unit_id = Column(
        "BusinessUnitId",
        String,
        ForeignKey("business_unit.business_unit_id"),
        nullable=True,
    )
    account_no = Column(
        "AccoutNo", String, ForeignKey("Account.account_no"), nullable=True
    )
    amount = Column("Amount", Float, nullable=True)
    currency_id = Column("CurrencyId", String, nullable=True)
    accounting_date = Column("AccountingDate", String, nullable=True)
    data_type = Column("DataType", String, nullable=True)
    remarks = Column("Remarks", String, nullable=True)


class Account(db.Model):
    __tablename__ = "Account"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    chart_id = Column("ChartId", Integer, nullable=True)
    account_no = Column("AccountNo", String, nullable=True)
    account = Column("Account", String, nullable=True)
    account_type = Column("AccountType", String, nullable=True)
    dr_cr = Column("DR_CR", String, nullable=True)
    posting_level = Column("PostingLevel", String, nullable=True)
    inter_company_flag = Column("InterCompanyFlag", String, nullable=True)
    security_status = Column("SecurityStatus", String, nullable=True)
    revaluation = Column("Revaluation", Integer, nullable=True)
    reconciliation = Column("Reconciliation", Integer, nullable=True)
    account_control_class = Column("AccountControlClass", String, nullable=True)
    class_description = Column("ClassDescription", String, nullable=True)
    conversion_type_id = Column("ConversionTypeId", String, nullable=True)
    conversion_type_description = Column(
        "ConversionTypeDescription", String, nullable=True
    )
    udf1 = Column("UDF1", String, nullable=True)
    xbrl_tag = Column("XBRLTag", String, nullable=True)
    user_created = Column("UserCreated", String, nullable=True)
    date_created = Column("DateCreated", String, nullable=True)


class RAD(db.Model):
    __tablename__ = "RAD"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    rad_type_id = Column("RADTypeId", String, nullable=True)
    rad_type = Column("RADType", String, nullable=True)
    rad_id = Column("RADId", String, nullable=True)
    rad = Column("RAD", String, nullable=True)


class BusinessUnit(db.Model):
    __tablename__ = "BusinessUnit"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    business_unit_id = Column("BusinessUnitId", String, nullable=True)
    business_unit = Column("BusinessUnit", String, nullable=True)
    company_id = Column("CompanyId", String, nullable=True)
    company = Column("Company", String, nullable=True)
    account_control_group_id = Column("AccountControlGroupId", String, nullable=True)
    account_control_group = Column("AccountControlGroup", String, nullable=True)
    rad_control_group_id = Column("RADControlGroupId", String, nullable=True)
    rad_control_group = Column("RADControlGroup", String, nullable=True)
    retained_business_unit_id = Column("RetainedBusinessUnitId", String, nullable=True)
    retained_business_unit = Column("RetainedBusinessUnit", String, nullable=True)
    retained_chart = Column("RetainedChart", String, nullable=True)
    retained_account_id = Column("RetainedAccountId", String, nullable=True)
    retained_account = Column("RetainedAccount", String, nullable=True)
    posting_level = Column("PostingLevel", String, nullable=True)
    security_status = Column("SecurityStatus", String, nullable=True)
    address_id = Column("AddressId", String, nullable=True)
    address = Column("Address", String, nullable=True)
    user_defined1 = Column("UserDefined1", String, nullable=True)
    user_defined2 = Column("UserDefined2", String, nullable=True)
    user_defined3 = Column("UserDefined3", String, nullable=True)
    user_defined4 = Column("UserDefined4", String, nullable=True)
    user_defined5 = Column("UserDefined5", String, nullable=True)
    user_defined6 = Column("UserDefined6", String, nullable=True)
    user_defined7 = Column("UserDefined7", String, nullable=True)
    user_defined8 = Column("UserDefined8", String, nullable=True)
    user_defined9 = Column("UserDefined9", String, nullable=True)
    user_defined10 = Column("UserDefined10", String, nullable=True)
    user_created = Column("UserCreated", String, nullable=True)
    date_created = Column("DateCreated", String, nullable=True)


class Budget(db.Model):
    __tablename__ = "Budget"

    id = Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False)
    budget_id = Column("BudgetId", String, nullable=True)
    business_unit_id = Column(
        "BusinessUnitId",
        Integer,
        ForeignKey("BusinessUnit.BusinessUnitId"),
        nullable=True,
    )
    chart_id = Column("ChartId", Integer, nullable=True)
    account_no = Column(
        "AccountNo", Integer, ForeignKey("Account.AccountNo"), nullable=True
    )
    amount = Column("Amount", Float, nullable=True)
    currency_id = Column("CurrencyId", String, nullable=True)
    base_amount = Column("BaseAmount", Float, nullable=True)
    business_unit = Column(
        "BusinessUnit", String, ForeignKey("BusinessUnit.BusinessUnit"), nullable=True
    )
    chart = Column("Chart", String, ForeignKey("Account.Chart"), nullable=True)
    account = Column("Account", String, ForeignKey("Account.Account"), nullable=True)
