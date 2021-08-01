// SHOP TEMPLATE
// Auto submit sort-by form
$(".sort-by-form").click(function(){
    $(this).submit();
})

// ADD ALBUM FORM
// Add tracklist input to AddAlbumForm
function renderNewInput(inputNumber){    
    // Only render a new input if the previous one has text content
    if ($(`#track_${inputNumber - 1}`).val() != ""){
        // Remove existing add and remove input buttons
        $(".fa-plus-circle").remove()
        $(".fa-minus-circle").remove()

        const newInputHtml = 
        `<label for="track_${inputNumber}" class="sr-only">Track ${inputNumber}</label>
        <input type="text" id="track_${inputNumber}" class="w-75 mb-1 add-track-input" placeholder="Enter track ${inputNumber}" required>
        <i class="fas fa-plus-circle ml-1 ml-sm-2 pointer" id="plus-btn-${inputNumber}" 
            title="Click to add another track" onclick="renderNewInput(${inputNumber + 1})"></i>
        <i class="fas fa-minus-circle ml-2 ml-sm-3 pointer" id="minus-btn-${inputNumber}"
            title="Click to remove track" onclick="removeInput(${inputNumber})"></i>`
    
        const tracklistContainer = $("#tracklist");
        tracklistContainer.append(newInputHtml);
    } 
    // else {  
    //    // Text input has no content - render a tooltip
    //     $(`#track_${inputNumber - 1}`).tooltip({
    //         title: "Please use this input first!"
    //     }).tooltip('show');
    //     clearTooltip($(`#track_${inputNumber - 1}`))
    // }
}

/* After 2.5 seconds, clear any tooltips */
function clearTooltip(tooltipContainer) {
    setTimeout(() => {
        tooltipContainer.tooltip('dispose');
    }, 2500);
}

// Remove tracklist input and render appropriate buttons on previous input
function removeInput(inputNumber){
    // Remove current input
    $(`#track_${inputNumber}`).remove();
    // Remove existing add and remove input buttons
    $(".fa-plus-circle").remove()
    $(".fa-minus-circle").remove()

    // Render a new plus button
    let newButtonsHtml = 
        `<i class="fas fa-plus-circle ml-1 ml-sm-2 pointer" id="plus-btn-${inputNumber}" 
            title="Click to add another track" onclick="renderNewInput(${inputNumber})"></i>`
    
    // As long as the input previous to the current input isn't input 1, render a minus button
    if(inputNumber > 2){
        newButtonsHtml +=
        `<i class="fas fa-minus-circle ml-2 ml-sm-3 pointer" id="minus-btn-${inputNumber}"
            title="Click to remove track" onclick="removeInput(${inputNumber - 1})"></i>`
    }
    $("#tracklist").append(newButtonsHtml);
}

// Format tracklist data and then submit form
$("#submit-album").click(function(event){
    // event.preventDefault()
    let formattedTracks = {};
    // Get all the data form the tracklist form inputs and format to JSON
    $(".add-track-input").each(function(index, track){
        let trackCount = index + 1
        const trackName = $(track).val().trim();
        formattedTracks[trackCount] = trackName;
    });
    // Get the hidden tracklist input and insert JSON tracklist before submitting
    console.log(typeof(formattedTracks));
    console.log(formattedTracks);
    const jsonTracks = JSON.stringify(formattedTracks)
    $("#id_tracklist").val(jsonTracks);
});