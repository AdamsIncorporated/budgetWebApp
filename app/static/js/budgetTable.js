function toggleRow(rowId) {
    const classId = `${rowId}-hidden-row`
    const rows = document.getElementsByClassName(classId);

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
        const cells = document.querySelectorAll(
            `tbody tr td:nth-child(${index})`
        );
        cells.forEach((cell) => {
            const isEvenRow = cell.parentElement.rowIndex % 2 === 0;
            const classToAdd = isEvenRow ? "bg-stone-200" : "bg-teal-200";
            highlight
                ? cell.classList.add(classToAdd)
                : cell.classList.remove(classToAdd);
        });
    }

    // add total event listener for each total budget element
    function updateTotalAmount() {
        const totals = document.querySelectorAll('td[total]');
        totals.forEach(function (field) {
            const row = field.closest('tr');
            const businessCaseAmount = row.querySelector('td[businessCase]').textContent;
            const proposedBudgetAmount = row.querySelector('td[proposedBudget]').textContent;
            const total = parseFloat(businessCaseAmount) + parseFloat(proposedBudgetAmount);
            field.textContent = total || 0;
        });
    }

    // Add change event listeners to the relevant fields
    const businessCaseFields = document.querySelectorAll('td[businessCase]');
    const proposedBudgetFields = document.querySelectorAll('td[proposedBudget]');

    businessCaseFields.forEach(function (field) {
        field.addEventListener('change', updateTotalAmount);
    });

    proposedBudgetFields.forEach(function (field) {
        field.addEventListener('change', updateTotalAmount);
    });

    // Optionally, if you're using inputs, you might want to listen for input or keyup events
    businessCaseFields.forEach(function (field) {
        field.addEventListener('input', updateTotalAmount);
    });

    proposedBudgetFields.forEach(function (field) {
        field.addEventListener('input', updateTotalAmount);
    });

    // Initial call to set totals based on existing values
    updateTotalAmount();


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
