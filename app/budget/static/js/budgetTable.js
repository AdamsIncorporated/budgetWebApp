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

    // add total event listener for each total budget element
    function updateTotalAmount(element) {
        const row = element.closest('tr');
        const businessCaseAmountElement = row.querySelector('input[sumbusinesscaseamount]');
        const proposedBudgetElement = row.querySelector('input[sumproposedbudget]');
        const totalBudget = row.querySelector('input[TotalBudget]');

        const businessCaseAmount = parseFloat(businessCaseAmountElement?.textContent || 0);
        const proposedBudgetAmount = parseFloat(proposedBudgetElement?.textContent || 0);
        const total = businessCaseAmount + proposedBudgetAmount;

        totalBudget.textContent = total.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }


    // Add change event listeners to the relevant fields
    const sumBusinessCaseAmounts = document.querySelectorAll('input[sumbusinesscaseamount]');
    const sumProposedBudgets = document.querySelectorAll('input[sumproposedbudget]');

    sumBusinessCaseAmounts.forEach(function (field) {
        field.addEventListener('input', function () {
            updateTotalAmount(field);
        });
    });

    sumProposedBudgets.forEach(function (field) {
        field.addEventListener('input', function () {
            updateTotalAmount(field);
        });
    });

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
