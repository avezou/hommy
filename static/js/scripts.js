// var myOptions = {
//     val1 : 'Blue',
//     val2 : 'Orange'
// };
// var mySelect = $('#myColors');
// $.each(myOptions, function(val, text) {
//     mySelect.append(
//         $('<option></option>').val(val).html(text)
//     );
// });

// var names = ["Bob Hope","James Jones","Steve Jobs","Larry McBridge"]   
// var query = "bo"
// var results = $(names)
//         .map(function(i,v){ 
//             if(v.toLowerCase().indexOf(query.toLowerCase())!=-1){return v} 
//         }).get()
$(document).ready(function(){
    $("#mySearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myList div").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });