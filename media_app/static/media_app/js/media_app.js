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

// Get comments when page loads
$(document).ready(getComments());

// Get JSON data containing list of comment objects
function getComments(page=1){
    const objectId = $("#single-id").text();
    $.ajax({
        url: `/media/get_comments`,
        type: "GET",
        data: {
            'objectID': objectId,
            'page': page,

        },
        dataType: 'json',
        success: function (data) {
            renderComments(data);
        },
        error: function(xhr,status,error){
            console.log(xhr,status,error)
        },
    })
}

function renderComments(data){
    let htmlContent = "";
    data.forEach(commentObj =>{
        htmlContent +=
            `<div class="row my-1 no-gutters">
                <div class="col-2">
                    <img class="profile-pic" src="${commentObj['posted_by_img']}" alt="The profile picture for ${commentObj['posted_by']}">
                </div>
                <div class="col-10 comment-container">
                    <p class="">
                        Comment by: ${commentObj['posted_by']} <br>
                        ${commentObj['text']}
                    </p>
                </div>
            </div>`
    });

    htmlContent += renderPaginationButtons(data[0])
    const commentDiv = $("#comment-section")
    if(commentDiv.html() != htmlContent){
        commentDiv.html(htmlContent);
    }
}

function renderPaginationButtons(data){
    let htmlContent = '';
    let nextPage = parseInt(data['current_page']) + 1
    let prevPage = parseInt(data['current_page']) - 1
    if (data['has_prev']){
        htmlContent += 
            `<button onclick="getComments(${prevPage})" class="btn custom-btn btn-outline-secondary">Previous</button>`
    }else {
        htmlContent += 
            `<button class="btn custom-btn btn-outline-secondary" disabled>Previous</button>`
    }
    if (data['has_next']){
        htmlContent += 
            `<button onclick="getComments(${nextPage})" class="btn custom-btn btn-outline-secondary">Next</button>`
    } else {
        htmlContent += 
            `<button class="btn custom-btn btn-outline-secondary" disabled>Next</button>`
        
    }

    return htmlContent
}
