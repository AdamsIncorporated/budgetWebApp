// Column highlighting event listener
document.addEventListener("DOMContentLoaded", () => {

    const headers = document.querySelectorAll("thead th");

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
            `tbody tr td:nth-child(${index + 6})`
        );
        cells.forEach((cell) => {
            const isEvenRow = cell.parentElement.rowIndex % 2 === 0;
            const classToAdd = isEvenRow ? "bg-stone-200" : "bg-teal-200";
            highlight
                ? cell.classList.add(classToAdd)
                : cell.classList.remove(classToAdd);
        });
    }

    function getColorForvariance(variance) {
        // Check if the value is negative or positive
        if (variance < 0) {
            return '#be123c'; // Red color for negative values
        } else {
            return '#047857'; // Green color for positive or zero values
        }
    }

    // Find all input fields whose ID contains "variance"
    const varianceFields = document.querySelectorAll('input[id*="Variance"]');

    varianceFields.forEach(function (field) {
        const varianceValue = parseFloat(field.value); // Assuming the value is a number

        if (!isNaN(varianceValue)) {
            const fontColor = getColorForvariance(varianceValue);
            field.style.color = fontColor;
            field.style.fontStyle = 'italic'; // Optional styling for italic text
        }
    });


    // add event listner for query button
    document.getElementById('queryBtn').addEventListener('click', () => {
        const fiscalYear = document.getElementById('fiscal_year_picklist').value;
        const businessUnitId = document.getElementById('business_unit_picklist').value;
        const fiscalYearInt = String(fiscalYear).replace('FY', '20');
        const uri = `/budget/budget-entry/${fiscalYearInt}/${businessUnitId}`;
        window.location.href = uri;
    });
});
