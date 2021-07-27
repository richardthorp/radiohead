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
    let textContent = '';
    const welcomeTextArea = $("#welcome-text");
    setTimeout(function(){
        welcomeTextArea.removeClass('big-welcome-text');
        textContent += 'Welcome';
        welcomeTextArea.text(textContent);
    }, 800);
    setTimeout(function(){
        textContent = " to";
        welcomeTextArea.text(textContent);
    }, 2000);
    setTimeout(function(){
        textContent = " the";
        welcomeTextArea.text(textContent);
    }, 2500);
    setTimeout(function(){
        textContent += " home";
        welcomeTextArea.text(textContent);
    }, 3000);
    setTimeout(function(){
        textContent += " of";
        welcomeTextArea.text(textContent);
    }, 3600);
    setTimeout(function(){
        textContent = " Radio";
        welcomeTextArea.text(textContent);
        welcomeTextArea.addClass('big-welcome-text');
    }, 5000);
    setTimeout(function(){
        textContent += "<br class='d-sm-none'>head";
        welcomeTextArea.html(textContent);
    }, 5800);
}

// Repeat welcome text animation
$(document).ready(function() {
    addWelcomeText();
    setInterval(() => {
        addWelcomeText();
    }, 10000)
})