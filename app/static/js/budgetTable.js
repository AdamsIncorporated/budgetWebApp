function displayError(element) {
    const errorTooltip = element.querySelector('.error-tooltip'); // Find the tooltip inside the td

    if (element && errorTooltip) {
        const rect = element.getBoundingClientRect();
        const tooltipHeight = errorTooltip.offsetHeight;

        // Position the tooltip slightly above the input field
        errorTooltip.style.left = `${rect.left}px`;
        errorTooltip.style.top = `${rect.top - tooltipHeight - 50}px`; // Adjust the position based on input field
        errorTooltip.classList.remove("hidden");
    }
}

function hideError(element) {
    const errorTooltip = element.querySelector('.error-tooltip'); // Find the tooltip inside the td

    if (errorTooltip) {
        errorTooltip.classList.add("hidden");
    }
}

function toggleRow(element, rowId) {
    const icon = element.querySelector('i');
    const classId = `${rowId}-hidden-row`
    const rows = document.getElementsByClassName(classId);

    icon.classList.toggle('fa-minus-square');
    icon.classList.toggle('fa-plus-square');

    [...rows].forEach((row) => {
        row.classList.toggle('hidden');
    });
}

document.addEventListener("DOMContentLoaded", () => {

    const headers = document.querySelectorAll("thead tr:nth-child(2) th");

    headers.forEach((header, index) => {
        header.addEventListener("mouseover", () =>
            toggleCellHighlight(index, true)
        );
        header.addEventListener("mouseout", () =>
            toggleCellHighlight(index, false)
        );
    });

    function toggleCellHighlight(index, highlight) {
        const adjustedForHiddenCellsIndex = index + 13
        const cells = document.querySelectorAll(
            `tbody tr td:nth-child(${adjustedForHiddenCellsIndex})`
        );
        cells.forEach((cell) => {
            const isEvenRow = cell.parentElement.rowIndex % 2 === 0;
            const classToAdd = isEvenRow ? "bg-stone-200" : "bg-teal-200";
            
            if (highlight) {
                cell.classList.add(classToAdd);
                cell.classList.add("border-none");
            } else {
                cell.classList.remove(classToAdd);
                cell.classList.remove("border-none");
            }
        });
    }

    // // add total event listener for each total budget element
    // function updateTotalAmount() {
    //     const totals = document.querySelectorAll('td[total]');
    //     totals.forEach(function (field) {
    //         const row = field.closest('tr');
    //         const businessCaseAmount = row.querySelector('*[id*="businessCase"]').textContent;
    //         const proposedBudgetAmount = row.querySelector('*[id*="proposedBudget"]').textContent;
    //         const total = parseFloat(businessCaseAmount) + parseFloat(proposedBudgetAmount);
    //         field.textContent = total || 0;
    //     });
    // }

    // // Add change event listeners to the relevant fields
    // const businessCaseFields = document.querySelectorAll('td[businessCase]');
    // const proposedBudgetFields = document.querySelectorAll('td[proposedBudget]');

    // businessCaseFields.forEach(function (field) {
    //     field.addEventListener('change', updateTotalAmount);
    // });

    // proposedBudgetFields.forEach(function (field) {
    //     field.addEventListener('change', updateTotalAmount);
    // });

    // // Optionally, if you're using inputs, you might want to listen for input or keyup events
    // businessCaseFields.forEach(function (field) {
    //     field.addEventListener('input', updateTotalAmount);
    // });

    // proposedBudgetFields.forEach(function (field) {
    //     field.addEventListener('input', updateTotalAmount);
    // });

    // // Initial call to set totals based on existing values
    // updateTotalAmount();


    // add event listner for query button
    document.getElementById('queryBtn').addEventListener('click', () => {
        const historicalFiscalYear = document.getElementById('historical_fiscal_year_picklist').value;
        const proposedFiscalYear = document.getElementById('proposed_fiscal_year_picklist').value;
        const businessUnitId = document.getElementById('business_unit_picklist').value;
        const base = `/budget/budget-entry/${businessUnitId}`
        const uri = base + `?historical_fiscal_year=${encodeURIComponent(historicalFiscalYear)}&proposed_fiscal_year=${encodeURIComponent(proposedFiscalYear)}`;
        window.location.href = uri;
    });
});
