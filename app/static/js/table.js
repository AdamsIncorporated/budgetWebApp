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
            `tbody tr td:nth-child(${index + 1})`
        );
        cells.forEach((cell) => {
            const isEvenRow = cell.parentElement.rowIndex % 2 === 0;
            const classToAdd = isEvenRow ? "bg-stone-200" : "bg-teal-200";
            highlight
                ? cell.classList.add(classToAdd)
                : cell.classList.remove(classToAdd);
        });
    }

    // Function to determine color based on percentage
    function getColorForPercent(percent) {
        const minValue = -100;
        const maxValue = 100;

        // Normalize percent value between 0 and 1
        const normalizedValue = (percent - minValue) / (maxValue - minValue);

        // Map normalized value to a color from red (low) to green (high)
        const red = Math.round(255 * (1 - normalizedValue));
        const green = Math.round(255 * normalizedValue);

        return `rgb(${red}, ${green}, 0)`;
    }

    // Find all input fields whose ID contains "Percent"
    const percentFields = document.querySelectorAll('input[id*="Percent"]');

    percentFields.forEach(function (field) {
        const percentValue = parseFloat(field.value); // Assuming the value is a number

        if (!isNaN(percentValue)) {
            const fontColor = getColorForPercent(percentValue);
            field.style.color = fontColor;
            field.style.fontStyle = 'italic';
        }
    });
});
