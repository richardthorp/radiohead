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
    setTimeout(function(){
        addWelcomeText();
        setInterval(() => {
            addWelcomeText();
        }, 10000)
    }, 100);
})

// Fix onscroll whitespace bug for background image on mobile
// Solution by Stack Overflow user 'Jason' from:
//https://stackoverflow.com/questions/24944925/background-image-jumps-when-address-bar-hides-ios-android-mobile-chrome
const bg = $(".main-site-bg")
function resizeBackground() {
    bg.height($(window).height() + 60);
}

$(window).resize(resizeBackground);
resizeBackground();

// Size iframe video player depending on sceen width
function resizeIframe() {
    const containerWidth = $(".video-container").width();
    const iFrame = $("#iFrame");
    const iFrameHeight = containerWidth * 0.67;

    iFrame.attr('height', iFrameHeight);
}

// Size iframe on document load
$(document).ready(function () {
    resizeIframe();
});

// Resize iframe when screen width changes
$(window).resize(function () {
    resizeIframe();
})

// Auto submit sort-by form
$(".sort-by-form").click(function(){
    $(this).submit();
})