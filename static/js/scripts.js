
function myToggle(e, b) {
    if (b) {
        e.show(300);
        e.parent().show(300);
    } else {
        e.hide("fast");
        e.parent().hide("fast");
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
$(document).ready(function() {
    // Refresh cards every 10 seconds
    setInterval(refreshCards, 15000);
});

function hashCode (str){
    var hash = 0;
    if (str.length == 0) return hash;
    for (i = 0; i < str.length; i++) {
        char = str.charCodeAt(i);
        hash = char % 360;
        console.log("modulo: " + hash)
        hash = hash + hash; // Convert to 32bit integer
    }
    return hash % 360;
};

var colo = 0
$(document).ready(function() {
    $("span.badge").each(function() {
        var spn = $(this);
        var spnId = spn.attr("id");
        if (spnId === undefined) {
            return;
        }
        console.log("spnId: " + spnId);
        var color = "hsl(" + ((colo + 360) * 360 / 360) + ", 100%, 75%)";
        console.log("color: " + color);
        spn.css("background-color", color);
        colo = colo + 20;
    });
});
function confirmDelete(id) {
    var r = confirm("Are you sure you want to delete this item?");
    if (r == true) {
        window.location.href = "/delete/" + id;
    }
}

// Additional script

