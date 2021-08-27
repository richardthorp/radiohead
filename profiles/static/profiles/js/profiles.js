// Format date in order history
$(document).ready(function(){
    let date = $(".order-date").text();
    const formattedDate = date.split(',').slice(0, 2);
    $(".order-date").text(formattedDate);
});