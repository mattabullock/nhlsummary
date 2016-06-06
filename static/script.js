$(function() {
    $.ajax({
        url:'data'
    }).done(function(data) {
        console.log(data);
        console.log(JSON.parse(data));
    });

});
