$(document).ready(function() {
    $(".review_submit").attr('disabled', true);
    
    $('textarea').on('keyup',function() {
        var textarea_value = $(".review_input").val();
        
        if(textarea_value != '') {
            $(".review_submit").attr('disabled', false);
        } else {
            $(".review_submit").attr('disabled', true);
        }
    });
});