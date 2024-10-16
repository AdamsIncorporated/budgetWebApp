document
    .getElementById("adminLoginBtn")
    .addEventListener("click", function () {
        window.location.href = "/auth/login";
    });

document.getElementById("getStarted").addEventListener("click", () => {
    const fiscalYear = document.getElementById("fiscalYear");
    const businessUnit = document.getElementById("businessUnit");
    const fiscalYearValue = String(fiscalYear.value).replace('FY', 20);
    const businessUnitValue = businessUnit.value;


    if (!fiscalYear.disabled && !businessUnit.disabled) {
        window.location.href = `budget/budget-entry/${fiscalYearValue}/${businessUnitValue}`
    }
});