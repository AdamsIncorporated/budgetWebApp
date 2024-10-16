$(document).ready(function () {
    const elements = $("input[masknumber]");
    
    // Initialize the input mask
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
        onblur: function () {
            const value = parseFloat($(this).val().replace(/,/g, ''));
            if (value > 1000000000) {
                $(this).val('1,000,000,000.00');
            }
        }
    });
});
