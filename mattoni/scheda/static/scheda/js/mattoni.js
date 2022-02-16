$(document).ready(function () {
    $('#pervieta_no').click(function (e) {
        e.preventDefault();
        
        $('#ostruzione').collapse('show');
        $('#pervieta_no').prop('checked', true);
        $('#pervieta_si').prop('checked', false);
    });
    $('#pervieta_si').click(function (e) {
        e.preventDefault();
        
        $('#ostruzione').collapse('hide');
        $('#pervieta_no').prop('checked', false);
        $('#pervieta_si').prop('checked', true);
    });
});

