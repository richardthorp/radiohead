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
        const formattedTime = formatTime(commentObj['time']);
        let commentPermissionshtml = "";
        if(commentObj['comment_permissions']) {
            commentPermissionshtml = `<p class="clear-font mb-2"><a href="">Edit comment</a> - <a href="">Delete comment</a></p>`
        }
        console.log(commentObj)
        htmlContent +=
            `<div class="row my-3 my-md-4 no-gutters">
                <div class="col-2 col-md-1">
                    <img class="profile-pic" src="${commentObj['posted_by_img']}" alt="The profile picture for ${commentObj['posted_by']}">
                </div>
                <div class="col-10 col-md-11 comment-container px-2 px-md-3">
                <p class="clear-font mb-2">
                    <strong>${commentObj['posted_by']}</strong> - ${formattedTime} <br>
                </p>
                    <p class="clear-font mb-2">
                        ${commentObj['text']}<br>
                    </p>
                    ${commentPermissionshtml}                    
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
    // Open a row div and a column div for the buttons
    let htmlContent = 
        `<div class="row">
            <div class="col-12 d-flex justify-content-center">`;

    let nextPage = parseInt(data['current_page']) + 1
    let prevPage = parseInt(data['current_page']) - 1
    // Render appropriate buttons depending on the data passed in from thr renderComments function above
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
    // Fianlly, close the row and column div elements
    htmlContent += 
        `</div>
        </div>`

    return htmlContent
}

function addComment(objectId, userId){
    const data = {
        'object_id': parseInt(objectId),
        'user_id': parseInt(userId),
        'comment': $("#id_text").val(),
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
    }
    $.post('/media/add_comment', data)
        .done(setTimeout(getComments, 500))
        .then($("#id_text").val(""));
}

function formatTime(dateTime){
    const splitDateTime = dateTime.split('T');
    const time = splitDateTime[1].slice(0, 5);
    const day = splitDateTime[0].split("-")[2];
    let month = splitDateTime[0].split("-")[1];
    const year = splitDateTime[0].split("-")[0];

    switch (month) {
      case '01':
        month = 'Jan';
        break;
      case '02':
        month = 'Feb';
        break;
      case '03':
        month = 'Mar';
        break;
      case '04':
        month = 'Apr';
        break;
      case '05':
        month = 'May';
        break;
      case '06':
        month = 'Jun';
        break;
      case '07':
        month = 'Jul';
        break;
      case '08':
        month = 'Aug';
        break;
      case '09':
        month = 'Sep';
        break;
      case '10':
        month = 'Oct';
        break;
      case '11':
        month = 'Nov';
        break;
      case '12':
        month = 'Dec';
        break;
    }
    return `${time}, ${day} ${month} ${year}`;
  }
