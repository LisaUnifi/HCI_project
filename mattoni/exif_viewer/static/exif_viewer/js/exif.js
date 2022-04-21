$(document).ready(function () {

    // INFO HOTKEYS 
    $('#settings').click(function () {
        $('#modal_settings').modal('show');
    });

    // GESTIONE IMMAGINI 
    $('#gestione_img').click(function () {
        $('#modal_gestione').modal('show');
    });

    $('#chiudi_modal_gestione').click(function () {
        $('#modal_gestione').modal('hide');
    });

    $('#gestione_carica').click(function () {
        $('#gestione_collapse').collapse('toggle');
    });

    $('#carica_file').click(function () {
        $('#upload').modal('show');
    });

    $('#chiudi_modal').click(function () {
        $('#upload').modal('hide');
    });

    $('#delete_file').click(function () {
        $('#delete').modal('show');
    });

    $('#chiudi_modal_delete').click(function () {
        $('#delete').modal('hide');
    });

    // GESTIONE ALBUM 
    $('#album_nuovo').click(function () {
        $('#modal_album').modal('show');
    });

    $('#chiudi_modal_album').click(function () {
        $('#modal_album').modal('hide');
    });

    $('#elimina_album').click(function () {
        $('#modal_elimina_album').modal('show');
    });

    $('#chiudi_modal_elimina_album').click(function () {
        $('#modal_elimina_album').modal('hide');
    });

    // GESTIONE GEOLOCALIZZAZIONE IMMAGINI
    $('#geoloc').click(function () {
        $('#maps').modal('show');
    });

    $('#search').click(function () {
        $('#mappa_elementi').collapse('hide');
        $('#panorama_elementi').collapse('hide');
        $('#search').prop('checked', true);
        $('#mappa').prop('checked', false);
        $('#pano').prop('checked', false);
    });

    $('#mappa').click(function () {
        $('#mappa_elementi').collapse('toggle');
        $('#panorama_elementi').collapse('hide');
        $('#search').prop('checked', false);
        $('#mappa').prop('checked', true);
        $('#pano').prop('checked', false);
    });

    $('#pano').click(function () {
        $('#mappa_elementi').collapse('hide');
        $('#panorama_elementi').collapse('toggle');
        $('#search').prop('checked', false);
        $('#mappa').prop('checked', false);
        $('#pano').prop('checked', true);
    });

    $('#chiudi_modal_maps').click(function () {
        $('#maps').modal('hide');
    });
      
});
   
  