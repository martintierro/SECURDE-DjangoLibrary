$(document).ready(function() {
    $(".review_submit").attr('disabled', true);
    $(".review_submit").css('color', '#969696');
            $(".review_submit").css('background', '#dedede');
    
    $('textarea').on('keyup',function() {
        var textarea_value = $(".review_input").val();
        
        if(textarea_value != '') {
            $(".review_submit").attr('disabled', false);
            $(".review_submit").css('color', 'white');
            $(".review_submit").css('background', 'black');
        } else {
            $(".review_submit").attr('disabled', true);
            $(".review_submit").css('color', '#969696');
            $(".review_submit").css('background', '#dedede');
        }
    });

    $('#search_input').on('keyup', function(){
        let search_value = $("#search_input").val();
        
    })
});