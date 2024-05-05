
$("#mySearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList div").filter(function() {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

$('select[id="myTags"]').change(function() {
    var value = $(this).val().toLowerCase();
    console.log("logging select: " +value);
    $("#myList div").filter(function() {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});
