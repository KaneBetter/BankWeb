$(document).ready(function () {
    $("#deposit").change(function () {
        const amount = $("#deposit").val();
        $("#deposit").val(parseFloat(amount).toFixed(2));
    })

    $("#withdraw").change(function () {
        const amount = $("#withdraw").val();
        $("#withdraw").val(parseFloat(amount).toFixed(2));
    })
})