$(document).ready(function () {
    const elements = $("input[masknumber]");
    elements.inputmask({
        alias: "numeric",
        prefix: '',
        groupSeparator: ',',
        autoGroup: true,
        digits: 2,
        digitsOptional: false,
        clearIncomplete: true,
        placeholder: "0.00",
        max: 1000000000,
        // Handle the 'blur' event to enforce the max value
        onblur: function () {
            const value = parseFloat($(this).val().replace(/,/g, ''));
            if (value > 1000000000) {
                $(this).val('1,000,000,000.00'); // Set the value to the max if exceeded
            }
        }
    });
});
