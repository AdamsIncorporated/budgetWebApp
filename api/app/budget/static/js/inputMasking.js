$(document).ready(function () {
    const elements = $("[masknumber]");
    
    elements.inputmask({
        alias: "numeric",
        prefix: '',
        groupSeparator: ',',
        autoGroup: true,
        digits: 2,
        digitsOptional: false,
        clearIncomplete: true,
        placeholder: "0.00",
        showMaskOnHover: false,
        max: 1000000000,
        onblur: function () {
            const value = parseFloat($(this).val().replace(/,/g, ''));
            if (value > 1000000000) {
                $(this).val('1,000,000,000.00');
            }
        }
    });
});
