const navbar = document.getElementById('navbar');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    if (window.scrollY > lastScrollY) {
        // Scrolling down
        navbar.style.transform = 'translateY(-100%)'; // Hide navbar
    } else {
        // Scrolling up
        navbar.style.transform = 'translateY(0)'; // Show navbar
    }
    lastScrollY = window.scrollY; // Update last scroll position
});

function getLogin() {
    window.location.href = "/auth/login";
}

function getBudgetEntry() {
    const fiscalYear = document.getElementById("fiscalYear");
    const businessUnit = document.getElementById("businessUnit");
    const fiscalYearValue = String(fiscalYear.value).replace('FY', 20);
    const businessUnitValue = businessUnit.value;

    if (!fiscalYear.disabled && !businessUnit.disabled) {
        window.location.href = `budget/budget-entry/${fiscalYearValue}/${businessUnitValue}`
    }
}