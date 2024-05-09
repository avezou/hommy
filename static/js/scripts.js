
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
    console.log("logging select: " +value);
    $("#myList div").filter(function() {
        var show = $(this).text().toLowerCase().indexOf(value) > -1;
        myToggle($(this), show);
    });
});

$('select[id="myCategories"]').change(function() {
    var value = $(this).val().toLowerCase();
    console.log("logging select: " +value);
    $("#myList div").filter(function() {
        var show = $(this).text().toLowerCase().indexOf(value) > -1;
        myToggle($(this), show);
    });
});
function refreshCards() {
    $.ajax({
        url: '/get_data',
        type: 'GET',
        success: function(response) {
            for (app, stat in response.value) {
                if ( $("span[id$=app]")[0] == true) {
                    if (stat) {
                        $(this).removeClass('dot gradient-red').addClass('dot gradient-green')
                    } else {
                        $(this).removeClass('dot gradient-green').addClass('dot gradient-red')
                    }
                }      
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
};
$(document).ready(function() {
    // Refresh cards every 5 seconds
    setInterval(refreshCards, 5000);
});
