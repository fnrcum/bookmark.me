$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/action_signup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});