window.onload = function() {
    var img_f = document.getElementById("img_front");
    var img_b = document.getElementById("img_back");

    var h = document.getElementById("hashtag");
    var ec = document.getElementById("ecs");
    var c = document.getElementById("circle");

    var canvas_front = document.getElementById("canvas_front");
    var canvas_back = document.getElementById("canvas_back");

    canvas_front.width = img_f.width;
    canvas_front.height = img_f.height;
    canvas_back.width = img_b.width;
    canvas_back.height = img_b.height;

    var ctx_f = canvas_front.getContext("2d");
    var ctx_b = canvas_back.getContext("2d");

    canvas_front.addEventListener("click", function(e) {
        draw_f(e);
    }, false);
    $('#Cancella_f').click(function() {
        erase_f();
    });

    canvas_back.addEventListener("click", function(e) {
        draw_b(e);
    }, false);
    $('#Cancella_b').click(function() {
        erase_b();
    });

    function draw_f(e) {
        var posX = e.offsetX-12;
        var posY = e.offsetY-12;
        if ($('#Dolore_f').prop('checked') == true) {
            ctx_f.drawImage(ec, posX, posY, 24, 24);
        };
        if ($('#Ustione_f').prop('checked') == true) {
            ctx_f.drawImage(h, posX, posY, 24, 24);
        };
        if ($('#Emorragia_f').prop('checked') == true) {
            ctx_f.drawImage(c, posX, posY, 24, 24);
        };
    };

    function draw_b(e) {
        var posX = e.offsetX-12;
        var posY = e.offsetY-12;
        if ($('#Dolore_b').prop('checked') == true) {
            ctx_b.drawImage(ec, posX, posY, 24, 24);
        };
        if ($('#Ustione_b').prop('checked') == true) {
            ctx_b.drawImage(h, posX, posY, 24, 24);
        };
        if ($('#Emorragia_b').prop('checked') == true) {
            ctx_b.drawImage(c, posX, posY, 24, 24);
        };
    };

    function erase_f() {
        ctx_f.clearRect(0, 0, canvas_front.width, canvas_front.height);
    };

    function erase_b() {
        ctx_b.clearRect(0, 0, canvas_back.width, canvas_back.height);
    };

    $('#Dolore_f').click(function () {
        $('#Dolore_f').prop('checked', true);
        $('#Ustione_f').prop('checked', false);
        $('#Emorragia_f').prop('checked', false);
        $('#Cancella_f').prop('checked', false);
    });
    $('#Ustione_f').click(function () {
        $('#Dolore_f').prop('checked', false);
        $('#Ustione_f').prop('checked', true);
        $('#Emorragia_f').prop('checked', false);
        $('#Cancella_f').prop('checked', false);
    });
    $('#Emorragia_f').click(function () {
        $('#Dolore_f').prop('checked', false);
        $('#Ustione_f').prop('checked', false);
        $('#Emorragia_f').prop('checked', true);
        $('#Cancella_f').prop('checked', false);
    });
    $('#Cancella_f').click(function () {
        $('#Dolore_f').prop('checked', false);
        $('#Ustione_f').prop('checked', false);
        $('#Emorragia_f').prop('checked', false);
        $('#Cancella_f').prop('checked', true);
    });

    $('#Dolore_b').click(function () {
        $('#Dolore_b').prop('checked', true);
        $('#Ustione_b').prop('checked', false);
        $('#Emorragia_b').prop('checked', false);
        $('#Cancella_b').prop('checked', false);
    });
    $('#Ustione_b').click(function () {
        $('#Dolore_b').prop('checked', false);
        $('#Ustione_b').prop('checked', true);
        $('#Emorragia_b').prop('checked', false);
        $('#Cancella_b').prop('checked', false);
    });
    $('#Emorragia_b').click(function () {
        $('#Dolore_b').prop('checked', false);
        $('#Ustione_b').prop('checked', false);
        $('#Emorragia_b').prop('checked', true);
        $('#Cancella_b').prop('checked', false);
    });
    $('#Cancella_b').click(function () {
        $('#Dolore_b').prop('checked', false);
        $('#Ustione_b').prop('checked', false);
        $('#Emorragia_b').prop('checked', false);
        $('#Cancella_b').prop('checked', true);
    });

};
