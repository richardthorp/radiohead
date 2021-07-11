const userIcon = $("#user-icon");
const bagIcon = $("#bag-icon");
const navToggle = $(".navbar-toggler");

// Hide other dropdowns when user-icon is clicked
userIcon.click(function(){
    $("#navbarNav").removeClass('show');
    $("#bag-summary").removeClass('show');
})

// Hide other dropdowns when bag-icon is clicked
bagIcon.click(function(){
    $("#navbarNav").removeClass('show');
    $("#account-dropdown").removeClass('show');
})

// Hide other dropdowns when main nav toggle is clicked
navToggle.click(function(){
    $("#account-dropdown").removeClass('show');
    $("#bag-summary").removeClass('show');
})
