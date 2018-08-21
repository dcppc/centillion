// submitting form with modal:
// https://stackoverflow.com/a/29068742
//
// closing a bootstrap modal with submit button:
// https://stackoverflow.com/a/33478107
//
// flask post data as json:
// https://stackoverflow.com/a/16664376

/* this function is called when the user submits
 * the feedback form. it submits a post request
 * to the flask server, which squirrels away the
 * feedback in a file.
 */
function submit_feedback() {
    // this function is called when submit button clicked
    // algorithm:
    // - check if text box has content
    // - check if happy/sad filled out

    var smile_active = $('#modal-feedback-smile-div').hasClass('smile-active');
    var frown_active = $('#modal-feedback-frown-div').hasClass('frown-active');
    if( !( smile_active || frown_active ) ) {
        alert('Please pick the smile or the frown.')
    } else if( $('#modal-feedback-textarea').val()=='' ) {
        alert('Please provide us with some feedback.')
    } else {
        var user_sentiment = '';
        if(smile_active) {
            user_sentiment = 'smile';
        } else {
            user_sentiment = 'frown';
        }
        var escaped_text = $('#modal-feedback-textarea').val();

        // prepare form data 
        var data = {
            sentiment : user_sentiment,
            content : escaped_text
        };
        // post the form. the callback function resets the form
        $.post("/feedback", 
            data, 
            function(response) {
                $('#myModal').modal('hide');
                $('#myModalForm')[0].reset();
                add_alert(response);
                frown_unclick();
                smile_unclick();
        });
    }
}


function add_alert(response) {
    str = ""
    str += '<div id="feedback-messages-container" class="container">';

    if (response['status']=='ok') {
        // if status is ok, use alert-success
        str += '    <div id="feedback-messages-alert" class="alert alert-success alert-dismissible fade in">';
    } else {
        // otherwise use alert-danger
        str += '    <div id="feedback-messages-alert" class="alert alert-danger alert-dismissible fade in">';
    }

    str += '        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>';
    str += '        <div id="feedback-messages-contianer" class="container-fluid">';
    str += '            <div id="feedback-messages-div" class="co-xs-12">';
    str += '                <p>'
    str += response['message'];
    str += '                </p>';
    str += '            </div>';
    str += '    </div>';
    str += '</div>';
    $('div#messages').append(str);
}


/* for those particularly wordy users... limit feedback to 1000 chars */
function cool_it() { 
    if($('#modal-feedback-textarea').val().length > 1100 ){
        $('#modal-too-long').show();
    } else {
        $('#modal-too-long').hide();
    }
}

/* smiley functions */
function smile_click() {
    $('#modal-feedback-smile-div').addClass('smile-active');
    $('#modal-feedback-smile-icon').addClass('smile-active');
}
function frown_click() {
    $('#modal-feedback-frown-div').addClass('frown-active');
    $('#modal-feedback-frown-icon').addClass('frown-active');
}
function smile_unclick() {
    $('#modal-feedback-smile-div').removeClass('smile-active');
    $('#modal-feedback-smile-icon').removeClass('smile-active');
}
function frown_unclick() {
    $('#modal-feedback-frown-div').removeClass('frown-active');
    $('#modal-feedback-frown-icon').removeClass('frown-active');
}

function smile() {
    frown_unclick();
    smile_click();
}
function frown() { 
    smile_unclick();
    frown_click();
}


/* for those particularly wordy users... limit feedback to 1100 chars */
// how to check n characters in a textarea
// https://stackoverflow.com/a/19934613
/*
$(document).ready(function() {

    $('#modal-feedback-textarea').on('change',function(event) {
        if($('#modal-feedback-textarea').val().length > 1100 ){
            $('#modal-too-long').show();
        } else {
            $('#modal-too-long').hide();
        }
    });

}
*/

