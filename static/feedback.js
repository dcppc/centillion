// submitting form with modal:
// https://stackoverflow.com/a/29068742
//
// closing a bootstrap modal with submit button:
// https://stackoverflow.com/a/33478107
//
// flask post data as json:
// https://stackoverflow.com/a/16664376

/* make the smile green */
function smile_click() {
    $('#modal-feedback-smile-div').addClass('smile-active');
    $('#modal-feedback-smile-icon').addClass('smile-active');
    $('#modal-feedback-frown-div').removeClass('frown-active');
    $('#modal-feedback-frown-icon').removeClass('frown-active');
}

/* make the frown red */
function frown_click() {
    $('#modal-feedback-smile-div').removeClass('smile-active');
    $('#modal-feedback-smile-icon').removeClass('smile-active');
    $('#modal-feedback-frown-div').addClass('frown-active');
    $('#modal-feedback-frown-icon').addClass('frown-active');
}

