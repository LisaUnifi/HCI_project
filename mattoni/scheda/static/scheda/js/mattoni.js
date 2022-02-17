$(document).ready(function () {
    $('#pervieta_no').click(function () {

        $('#ostruzione').collapse('show');
        $('#pervieta_no').prop('checked', true);
        $('#pervieta_si').prop('chedked', false);
    });
    $('#pervieta_si').click(function () {
        $('#ostruzione').collapse('hide');
        $('#pervieta_no').prop('checked', false);
        $('#pervieta_si').prop('chedked', true);
        $('#ostruzione_no').prop('checked', false);
        $('#ostruzione_si').prop('checked', false);
    });

    $('#dolore_toracico_si').click(function () {

        $('#torace').collapse('show');
        $('#dolore_toracico_si').prop('checked', true);
        $('#dolore_toracico_no').prop('chedked', false);
    });
    $('#dolore_toracico_no').click(function () {
        $('#torace').collapse('hide');
        $('#dolore_toracico_si').prop('checked', false);
        $('#dolore_toracico_no').prop('chedked', true);
        $('#tipo_dolore_si').prop('checked', false);
        $('#tipo_dolore_no').prop('checked', false);
        $('#ora_dolore').val('');
        $('#data_dolore').val('');
    });
    
    $('#cincinnaty').click(function (e) {
        e.preventDefault();
        
        $('#cincinnaty_scheda').collapse('toggle');
        $('#forza_sensibilita_scheda').collapse('hide');
    });
    $('#forza_sensibilita').click(function (e) {
        e.preventDefault();
        
        $('#cincinnaty_scheda').collapse('hide');
        $('#forza_sensibilita_scheda').collapse('toggle');
    });

});

