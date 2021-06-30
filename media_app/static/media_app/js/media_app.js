// Size iframe video player depending on sceen width
function resizeIframe(){
    const containerWidth = $(".video-container").width();
    const iFrame = $("#iFrame");
    const iFrameHeight = containerWidth * 0.67;

    iFrame.attr('height', iFrameHeight);
}

// Size iframe on document load
$(document).ready(function() {
    resizeIframe();
});

// Resize iframe when screen width changes
$(window).resize(function(){
    resizeIframe();
})
