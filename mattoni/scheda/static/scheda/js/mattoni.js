$(document).ready(function () {

    $('#cosciente_no').click(function () {
        $('#centrale').modal('show');
        $('#cosciente_no').prop('checked', true);
        $('#cosciente_si').prop('checked', false);
    });

    $('#cosciente_si').click(function () {
        $('#blsd').collapse('hide');
        $('#cosciente_no').prop('checked', false);
        $('#cosciente_si').prop('checked', true);
        $('#respiraBLS_no').prop('checked', false);
        $('#respiraBLS_si').prop('checked', false);
        $('#circoloBLS_no').prop('checked', false);
        $('#circoloBLS_si').prop('checked', false);
        $('#dae_no').prop('checked', false);
        $('#dae_si').prop('checked', false);
    });

    $('#respiraBLS_si').click(function () {
        if($('#circoloBLS_no').prop('checked')){
            $('#msg_respiro').prop('hidden', true);
            $('#msg_circolo').prop('hidden', true);
            $('#msg_cicli').prop('disabled', true);
            $('#plus').prop('disabled', true);
            $('#minus').prop('disabled', true);
            $('#circoloBLS_no').prop('checked', false);
            $('#circoloBLS_si').prop('checked', true);
        }
    });

    $('#circoloBLS_si').click(function () {
        $('#msg_cicli').prop('disabled', true);
        $('#plus').prop('disabled', true);
        $('#minus').prop('disabled', true);
        $('#msg_respiro').prop('hidden', false);
        $('#msg_circolo').prop('hidden', true);
    });
    $('#circoloBLS_no').click(function () {
        $('#msg_cicli').prop('disabled', false);
        $('#plus').prop('disabled', false);
        $('#minus').prop('disabled', false);
        $('#msg_circolo').prop('hidden', false);
        $('#msg_respiro').prop('hidden', true);
        $('#respiraBLS_no').prop('checked', true);
        $('#respiraBLS_si').prop('checked', false);
    });

    $('#pervieta_no').click(function () {
        $('#ostruzione').collapse('show');
        $('#pervieta_no').prop('checked', true);
        $('#pervieta_si').prop('checked', false);
    });

    $('#pervieta_si').click(function () {
        $('#ostruzione').collapse('hide');
        $('#pervieta_no').prop('checked', false);
        $('#pervieta_si').prop('checked', true);
        $('#ostruzione_no').prop('checked', false);
        $('#ostruzione_si').prop('checked', false);
    });

    $('#sudato_si').click(function () {
        $('#freddo').collapse('show');
        $('#sudato_no').prop('checked', false);
        $('#sudato_si').prop('checked', true);
    });

    $('#sudato_no').click(function () {
        $('#freddo').collapse('hide');
        $('#sudato_no').prop('checked', true);
        $('#sudato_si').prop('checked', false);
        $('#sudato_freddo_no').prop('checked', false);
        $('#sudato_freddo_si').prop('checked', false);
    });

    $('#dolore_toracico_si').click(function () {
        $('#torace').collapse('show');
        $('#dolore_toracico_si').prop('checked', true);
        $('#dolore_toracico_no').prop('checked', false);
    });

    $('#dolore_toracico_no').click(function () {
        $('#torace').collapse('hide');
        $('#dolore_toracico_si').prop('checked', false);
        $('#dolore_toracico_no').prop('checked', true);
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

    $('#tp_front').click(function (e) {
        e.preventDefault();
        
        $('#tp_scheda_front').collapse('toggle');
        $('#tp_scheda_back').collapse('hide');
    });

    $('#tp_back').click(function (e) {
        e.preventDefault();
        
        $('#tp_scheda_front').collapse('hide');
        $('#tp_scheda_back').collapse('toggle');
    });

    $('#presa_visione').click(function () {
        $('#risposta_centrale').modal('hide');
        window.location.href = '#esito_menu';
    });

});

