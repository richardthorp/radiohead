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

// Initialise toasts
$('.toast').toast('show');

// Welcome text animation
function addWelcomeText(){
    let htmlContent = '';
    const welcomeTextArea = $("#welcome-text");
    setTimeout(function(){
        welcomeTextArea.removeClass('big-welcome-text');
        htmlContent += 'Welcome';
        welcomeTextArea.html(htmlContent);
    }, 800);
    setTimeout(function(){
        htmlContent = "to";
        welcomeTextArea.html(htmlContent);
    }, 2000);
    setTimeout(function(){
        htmlContent = "the <span class='d-hidden'>home of</span>";
        welcomeTextArea.html(htmlContent);
    }, 2500);
    setTimeout(function(){
        htmlContent = "the home <span class='d-hidden'>of</span>";
        welcomeTextArea.html(htmlContent);
    }, 3000);
    setTimeout(function(){
        htmlContent = "the home of";
        welcomeTextArea.html(htmlContent);
    }, 3600);
    setTimeout(function(){
        htmlContent = "Radio ";
        welcomeTextArea.html(htmlContent);
        welcomeTextArea.addClass('big-welcome-text');
    }, 5000);
    setTimeout(function(){
        htmlContent = "Radio<br class='d-sm-none'>head";
        welcomeTextArea.html(htmlContent);
    }, 5800);
}

// Repeat welcome text animation
$(document).ready(function() {
    addWelcomeText();
    setInterval(() => {
        addWelcomeText();
    }, 10000)
})