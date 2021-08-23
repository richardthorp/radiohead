// Auto resize textarea inputs when user types.
// Code copied from https://stackoverflow.com/questions/2948230/auto-expand-a-textarea-using-jquery User: SpYk3HH
$("textarea").keyup(function(e) {
    while($(this).outerHeight() < this.scrollHeight + parseFloat($(this).css("borderTopWidth")) + parseFloat($(this).css("borderBottomWidth"))) {
        $(this).height($(this).height()+1);
    };
});

// Get comments when page loads
$(document).ready(getComments());

// Get JSON data containing list of comment objects
function getComments(page=1){
    const objectId = $("#post-id").text();
    const postType = $("#post-type").text();
    $.ajax({
        url: `/portal/get_portal_comments`,
        type: "GET",
        data: {
            'object_id': objectId,
            'post_type': postType,
            'page': page,
        },
        dataType: 'json',
        success: function (data) {
            renderComments(data);
        },
        error: function(){
            $("#comment-section").html("<p>Sorry, we're having touble loading comments at the moment.</p>")
        },
    })
}

function renderComments(data){
    if (data.length == 0){
        $("#comment-section").html(`<p class="text-center">This video currently has no comments.</p>`);
        return;
    }
    let htmlContent = "";
    data.forEach(commentObj =>{
        const formattedTime = formatTime(commentObj['time']);
        // If the current user wrote the comment, generate the HTML to render edit and
        // to button delete buttons and insert into the htmlContent string below.
        let commentPermissionshtml = "";
        if(commentObj['comment_permissions']) {
            commentPermissionshtml = 
                `<p class="mb-2">
                    <a onclick="renderEditCommentSection(this, ${commentObj['id']})"
                        id="edit" class="comment-permissions">Edit comment</a> - 
                    <a onclick="renderDeleteButton(this, ${commentObj['id']})"
                    class="comment-permissions">Delete comment</a>
                </p>`
        }
        // If the comment has been edited, generate the below html and insert
        // into the htmlContent string below.
        let edited = "";
        if (commentObj['edited']){
            edited = "<span class='text-muted'>- (edited)</span>";
        }
        htmlContent +=
            `<div class="row my-3 my-md-4 no-gutters">
                <div class="col-2 col-md-1">
                    <img class="profile-pic" src="${commentObj['posted_by_img']}" alt="The profile picture for ${commentObj['posted_by']}">
                </div>
                <div class="col-10 col-md-11 comment-container px-2 px-md-3">
                <p class="mb-0 mb-sm-1">
                    <strong>${commentObj['posted_by']}</strong> - ${formattedTime} ${edited}
                </p>
                    <p class="comment-text  mb-0 mb-sm-1">
                        ${commentObj['text']}<br>
                    </p>
                    ${commentPermissionshtml}                    
                </div>
            </div>`
    });
    // Using the first comment object passed into the function, generate the pagination
    // buttons using the renderPaginationButtons() function defined below
    htmlContent += renderPaginationButtons(data[0])

    // Add a hidden div containing the current page number. This is to pass into the getComments()
    // functions in the 'Cancel' buttons in edit/delete sections.
    const currentPage = data[0]['current_page'];
    htmlContent += 
        `<div class="d-none current-page">${currentPage}</div>`

    // If the newly defined htmlString is different to the HTML currently on the page,
    // replace the HTML with the htmlString.
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
    // Render appropriate buttons depending on the data passed in from the renderComments function above
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
    // Prevent empty text box being submitted
    if ($("#add-comment-input").val() == ""){
        $("#add-comment-errors").text('You cannot submit an empty comment!');
        return;
    }else {
        const postType = $('#post-type').text();
        $("#add-comment-errors").text("");
        const data = {
            'post_type': postType,
            'post_id': parseInt(objectId),
            'user_id': parseInt(userId),
            'comment': $("#add-comment-input").val(),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        }
        $.post('/portal/add_portal_comment', data)
            .done(setTimeout(getComments, 500))
            .then($("#add-comment-input").val(""));
    }
}

function renderEditCommentSection(clickedLink, commentId){
    const commentArea = $(clickedLink).parent().parent();
    const existingComment = commentArea.children('.comment-text').text().trim();
    const currentPage = $(".current-page").text();
    const TextAreaHtml = 
        `<textarea id="edit-comment-input">${existingComment}</textarea>
        <p id="edit-comment-errors" class="text-danger mb-1"></p>
        <div class="mb-2">
            <button onclick="getComments(${currentPage})" class="btn custom-btn btn-outline-secondary">Cancel</button>
            <button onclick="submitEditedComment(${commentId})" class="custom-btn btn btn-dark">Edit Comment</button>
        </div>`
    commentArea.html(TextAreaHtml);
}

function submitEditedComment(commentId){
    const editedComment = $("#edit-comment-input").val()
    const postType = $('#post-type').text()
    if (editedComment == ""){
        $("#edit-comment-errors").text('You can not submit an empty comment!');
        return;
    } else {
        $("#edit-comment-errors").text("");
        const data = {
            'post_type': postType,
            'comment_id': parseInt(commentId),
            'edited_comment': editedComment,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        }
        $.post('/portal/edit_portal_comment', data)
            .done(setTimeout(getComments, 500));
    }
}

function renderDeleteButton(clickedLink, commentId){
    const editAndDeleteRow = $(clickedLink).parent();
    const currentPage = $(".current-page").text();
    const confirmDeleteHtml = 
        `<hr class="my-2 mx-auto">
        <p id="delete-confirmation" class="mb-2 font-weight-bold">Are you sure you want to delete this comment?</p>
        <div>
            <button onclick="getComments(${currentPage})" class="btn custom-btn btn-outline-secondary">Cancel</button>
            <button onclick="deleteComment(${commentId})" class="btn custom-btn btn-outline-danger">Delete</button>
        </div>
        `
    
    editAndDeleteRow.html(confirmDeleteHtml);
}

function deleteComment(commentId){
    const postType = $('#post-type').text()
    const data = {
        'post_type': postType,
        'comment_id': parseInt(commentId),
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
    }
    $.post('/portal/delete_portal_comment', data)
        .done(setTimeout(getComments, 500));
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
