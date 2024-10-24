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
    const businessUnit = document.getElementById("businessUnit");
    const businessUnitValue = businessUnit.value;

    if (!businessUnit.disabled) {
        window.location.href = `budget/budget-entry/${businessUnitValue}`
    }
}