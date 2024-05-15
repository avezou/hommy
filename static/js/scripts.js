
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
    $("span.dot").each(function() {
        var spn = $(this);
        var spnId = spn.attr("id");
        var spnUrl = spn.attr("data-url");
        console.log("spnUrl: " + spnUrl);
        
        $.ajax({spnUrl,
            type: "HEAD",
            timeout: 3000, 
            statusCode: {
                200: function() {
                    console.log("working : " + 200);
                    spn.addClass("gradient-green").removeClass('gradient-red');        
                },
                404: function() {
                    spn.addClass("gradient-red").removeClass('gradient-green');        
                },
                0: function() {
                    spn.addClass("gradient-red").removeClass('gradient-green');        
                }
            }
        });
    });
};
$(document).ready(function() {
    // Refresh cards every 10 seconds
    setInterval(refreshCards, 10000);
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

