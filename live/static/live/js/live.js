//  Reformat date to UK format
$(document).ready(function(){
    let dates = $(".gig-date");
    dates.each(function(){
        const date = $(this).text();
        const formattedDate = date.trim().split("-").reverse().join("-");
        $(this).text(formattedDate);
    });
});


/* Response table JS copied from 
https://bootstrapcreative.com/pattern/responsive-tables-that-stacks-on-mobile-instead-of-horizontal-scroll/ */
$(document).ready(function () {
    $('.table-responsive-stack').each(function (i) {
        var id = $(this).attr('id');
        $(this).find("th").each(function (i) {
            $('#' + id + ' td:nth-child(' + (i + 1) + ')').prepend('<span class="table-responsive-stack-thead">' + $(this).text() + ':</span> ');
            $('.table-responsive-stack-thead').hide();
        });
    });
    $('.table-responsive-stack').each(function () {
        var thCount = $(this).find("th").length;
        var rowGrow = 100 / thCount + '%';
        $(this).find("th, td").css('flex-basis', rowGrow);
    });
    function flexTable() {
        if ($(window).width() < 769) {
            $(".table-responsive-stack").each(function (i) {
                $(this).find(".table-responsive-stack-thead").show();
                $(this).find('thead').hide();
            });
        } else {
            $(".table-responsive-stack").each(function (i) {
                $(this).find(".table-responsive-stack-thead").hide();
                $(this).find('thead').show();
            });
        }
    }
    flexTable();
    window.onresize = function (event) {
        flexTable();
    };
});