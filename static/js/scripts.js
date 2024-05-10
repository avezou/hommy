
function myToggle(e, b) {
    if (b) {
        e.show(2000);
        e.parent().show(2000);
    } else {
        e.hide("slow");
        e.parent().hide("slow");
    }
}

$("#mySearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myList div").filter(function() {
        var show = $(this).text().toLowerCase().indexOf(value) > -1;
        myToggle($(this), show);
    });
});


$('select[id="myTags"]').change(function() {
    var value = $(this).val().toLowerCase();
    $("#myList div").filter(function() {
        var show = $(this).text().toLowerCase().indexOf(value) > -1;
        myToggle($(this), show);
    });
});

$('select[id="myCategories"]').change(function() {
    var value = $(this).val().toLowerCase();
    $("#myList div").filter(function() {
        var show = $(this).text().toLowerCase().indexOf(value) > -1;
        myToggle($(this), show);
    });
});
function refreshCards() {
    // AJAX call to fetch data from Flask backend
$.ajax({
    url: '/get_data',
    type: 'GET',
    success: function(response) {
        $("span.dot").each(function() {
            var spn = $(this);
            var spnId = spn.attr("id");
            if (response[spnId] == 1) {
                spn.addClass("gradient-green").removeClass('gradient-red');
            } else {
                spn.addClass("gradient-red").removeClass('gradient-green');
            }
        });
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
})};
var g = 0
$(document).ready(function() {
    // Refresh cards every 10 seconds
    console.log("refreshCards" + g++);
    setInterval(refreshCards, 10000);
});

// Additional script

