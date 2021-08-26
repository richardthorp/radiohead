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
        }, 10000);
    }, 200);
});