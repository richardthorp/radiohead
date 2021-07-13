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

function getComments() {
    let singleId = $("#single-id").text();
    const url = `/media/get_comments/${singleId}`;
    let response = fetch(url)
        .then(response => response.text())
        .then(data => {
            return data;
        })
    return response;
};

function renderComments() {
    let htmlContent = '';
    const commentDiv = $("#comment-section")
    getComments()
        .then(commentsString => {
            let comments = JSON.parse(commentsString);
            comments.forEach(commentObj => {
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
            if(commentDiv.html() != htmlContent){
                console.log('DIFF');
                commentDiv.html(htmlContent);
            }
        });
}

// $(document).ready(function(){
//     setInterval(renderComments, 4000)
// })

// {
//     'time': time,
//     'posted_by': posted_by.user.username,
//     'posted_by_img': posted_by_img,
//     'text': comment['fields']['text']
// }