window.onload = function() {
    var img_f = document.getElementById("img_front");
    var img_b = document.getElementById("img_back");

    var c = document.getElementById("circle");
    var h = document.getElementById("hashtag");
    var ec = document.getElementById("ecs");

    var canvas_front = document.getElementById("canvas_front");
    var canvas_back = document.getElementById("canvas_back");

    canvas_front.width = img_f.width;
    canvas_front.height = img_f.height;
    canvas_back.width = img_b.width;
    canvas_back.height = img_b.height;

    var ctx_f = canvas_front.getContext("2d");
    var ctx_b = canvas_back.getContext("2d");

    canvas_front.addEventListener("mousedown", draw);

    function draw(e) {
        var posX = e.clientX;
        var posY = e.clientY;

        ctx_f.drawImage(ec, posX, posY);
    };

};