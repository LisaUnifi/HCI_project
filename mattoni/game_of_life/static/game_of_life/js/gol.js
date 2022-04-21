

class Grid {
    constructor(rows, columns){
        this.rows = rows;
        this.columns = columns;
        this.cells = new Array(rows);
        this.initialx = [0,1,-1,0,0];
        this.initialy = [-1,-1,0,0,1];
        for(var i=0; i<rows;i++){
            this.cells[i] = new Uint8Array(columns);
            for(var j=0;j<columns;j++){
                this.cells[i][j] = 0;
            }
        }
        for(var i=0; i<this.initialx.length;i++){
            this.cells[(rows/2)+this.initialx[i]][(columns/2)+this.initialy[i]] = 1;
        }
    }

    //create a cell
    createCell(r,c){
        this.cells[r][c] = 1;
    }


    //delete a cell
    deleteCell(r,c){
        this.cells[r][c]=0;
    }


    //create a cell
    switchCell(r,c){
        if(this.cells[r][c]>0){
            this.deleteCell(r,c);
        }else{
            this.createCell(r,c);
        }
        return this.cells[r][c];
        
        //se fare altre cose, aggiungere altro
    }


    //count neighbors
    countNeighbors(r,c){
        var sum = 0;
        sum = (this.isAlive(r-1,c-1) + this.isAlive(r-1,c) + this.isAlive(r-1,c+1) + //precedent row
        this.isAlive(r,c-1) + this.isAlive(r,c+1) + //current row
        this.isAlive(r+1,c-1) + this.isAlive(r+1,c) + this.isAlive(r+1,c+1)); //successive row
        return sum;
    }

    //controls if cell x,y is alive
    isAlive(x, y)
    {
        if (x < 0 || x >= this.columns || y < 0 || y >= this.rows){
            return 0;
        }else if(this.cells[x][y]==0)
            return 0;
        

        return 1;
    }

    
    //random grid
    randomizeGrid(t){
        for(var i=0;i<this.rows;i++){
            for(var j=0;j<this.columns;j++){
                if(Math.random()>t){
                    this.cells[i][j] = 1;
                }else{
                    this.cells[i][j] = 0;
                }
            }
        }
    }


    //clear grid
    clearGrid(){
        for(var i=0;i<this.rows;i++){
            for(var j=0;j<this.columns;j++){
                
            this.cells[i][j] = 0;

            }
        }
    }


   


    //afunction that computes which cells will be alive of dead in the next age, also computing the age of each cell
    nextAge(){
        var changed = [];
        var k=0;
        for(var i=0;i<this.rows;i++){
            for(var j=0;j<this.columns;j++){
                var count = this.countNeighbors(i,j);
                if((count>3 && this.cells[i][j]>0) || (count<2 && this.cells[i][j]>0)){
                    changed[k]=i;
                    changed[k+1]=j;
                    k=k+2;
                }else if(count==3 && this.cells[i][j]==0){
                    changed[k]=i;
                    changed[k+1]=j;
                    k=k+2;
                }else if((count==2 || count==3) && (this.cells[i][j]>0 && this.cells[i][j]<9)){
                    this.cells[i][j] += 1;
                }
            }
        }

        //change now the states at the same time
        for(var i=0;i<k;i=i+2){
            this.switchCell(changed[i],changed[i+1])
        }

        //pass this to the controller, so that it can change the view...
        //this could be called directly by the controller when the system is not paused
        return changed;
    }


}





//CONTROLLER, add the logic to control the MODEL and the VIEW, making the data dialogue between the two


class Controller {
    constructor(){
        this.rows = 500;
        this.cols = 500;
        this.gol_grid = new Grid(this.rows,this.cols);
        this.interface = new View(this.rows,this.cols);
        this.interface.redraw(this.gol_grid.cells);
        this.bindHandlers();
        this.running = false;
    }

    bindHandlers(){
        this.interface.bindMouseDown(this.mouseDownHandler);
        this.interface.bindMouseMove(this.mouseMoveHandler);
        this.interface.bindMouseUp(this.mouseUpHandler);
        this.interface.bindDOMMouseScroll(this.scrollHandler);
        this.interface.bindMouseWheel(this.scrollHandler);
        this.interface.bindStartClick(this.btnStartHandler);
        this.interface.bindRandomClick(this.btnRandomHandler);
        this.interface.bindClearClick(this.btnClearHandler);
        this.interface.rangeListener(this.rangeHandler);
    }


    //Handlers from here. The interface get the events and they are passed to the controller
    //Here there are handlers that specify how to react to every event that may arise from the view
    
    //handles clicks on canvases, to draw cells
    canvasClickHandler = (e) => {
        var pos = this.mousePos(e);
        if(pos[0]){
            var alive = this.gol_grid.switchCell(pos[1],pos[2]);
            //colorare quadratino
            this.interface.redraw(this.gol_grid.cells);
        }
        
        
    }

    //function used to specify which cell was clicked using the mouse, to draw 
    mousePos(e){
        var x , y, posx, posy, cellsize=(this.interface.cellsize+1),cellspace=(this.interface.cellspace);
        var initscale = this.interface.initialscale;
        var rect = this.interface.grid.getBoundingClientRect();
        var event = e;




        posx = (event.clientX - rect.left)*initscale;
        posy = (event.clientY - rect.top)*initscale;

        [posx,posy] = this.interface.screen_to_grid(posx,posy);
        
        if((posx >= 0 && posx <= (this.interface.grid.width)) && (posy >= 0 && posy <= (this.interface.grid.height)) ){
            x = Math.ceil(((posx)/cellsize/cellspace) - 1);
            y = Math.ceil(((posy)/cellsize/cellspace) - 1);

            return [true, x, y];
        }else{
            return [false, 0,0];
        }
        

        

    }


    //handles the mouse down event on the canvas, to control the canvas panning
    mouseDownHandler = (e) => {
        document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
        //[this.interface.lastX,this.interface.lastY] = this.interface.screen_to_grid(e.offsetX || (e.pageX - this.interface.grid.offsetLeft), e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        this.interface.dragStart = [this.interface.lastX,this.interface.lastY];
        this.interface.dragged = false;
    }

    //handles the mouse movement on the canvas, to control the canvas panning
    mouseMoveHandler = (e) => {
        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        this.interface.dragged = true;  
        if (this.interface.dragStart){
            this.interface.offsetX = this.interface.offsetX + (this.interface.lastX - this.interface.dragStart[0])/this.interface.scalex/this.interface.initialscale;
            this.interface.offsetY = this.interface.offsetY + (this.interface.lastY - this.interface.dragStart[1])/this.interface.scaley/this.interface.initialscale;
            this.interface.dragStart = [this.interface.lastX,this.interface.lastY];

            this.interface.redraw(this.gol_grid.cells);
        }
    }

    
     //handles the mouse up event on the canvas, to control the canvas panning
    mouseUpHandler = (e) => {
        this.interface.dragStart = null;
        if (!this.interface.dragged) this.canvasClickHandler(e);
    }

    //handles the scroll of the mouse to control the zoom of the interface
    scrollHandler = (e) => {
        var delta = e.wheelDelta ? e.wheelDelta/200 : e.detail ? -e.detail : 0;
        if (delta) this.zoom(delta,e);
        return e.preventDefault() && false;
    }

    
    //controls how much the zoom must be, relative to the scroll that is used with the mouse
    zoom(clicks,e){
        let MAX_ZOOM = 3;
        let MIN_ZOOM = 1;

        var factor = Math.pow(this.interface.scalefactor,clicks);
        var azx, azy, bzx, bzy;

        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        [bzx, bzy]= this.interface.screen_to_grid(this.interface.lastX,this.interface.lastY);

        if(this.interface.scalex*factor>=MIN_ZOOM && this.interface.scalex*factor<=MAX_ZOOM){
            this.interface.scalex = this.interface.scalex*factor;
            this.interface.scaley = this.interface.scaley*factor;
        }else if(this.interface.scalex*factor<MIN_ZOOM){
            this.interface.scalex = this.interface.scalex;
            this.interface.scaley = this.interface.scaley;
        }else if(this.interface.scalex*factor>MAX_ZOOM){
            this.interface.scalex = this.interface.scalex;
            this.interface.scaley = this.interface.scaley;
        }

        
        this.interface.redraw(this.gol_grid.cells);

        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);

        [azx, azy] = this.interface.screen_to_grid(this.interface.lastX,this.interface.lastY);

        
        
        this.interface.offsetX = this.interface.offsetX - ((bzx-azx)/this.interface.scalex/(this.interface.initialscale));
        this.interface.offsetY = this.interface.offsetY - ((bzy-azy)/this.interface.scaley/(this.interface.initialscale));

        
        
        
    }

    //handler to clicking on start button
    btnStartHandler= (e) => {
        if(this.running){
            this.running = false;
            this.interface.btnstart.innerText = "Start";
        }        
        else{
            this.running = true;
            this.interface.btnstart.innerText = "Pause";
        }
        window.requestAnimationFrame(() => this.gameLoop());
            
    }

    //handler to clicking on random button
    btnRandomHandler= (e) => {
        this.gol_grid.randomizeGrid(0.8);
        this.interface.redraw(this.gol_grid.cells)
    }

    //handler to clicking on clear button
    btnClearHandler= (e) => {
        this.gol_grid.clearGrid();
        this.interface.redraw(this.gol_grid.cells)
    }


    rangeHandler= (e) => {
        this.interface.update_fps();
    }

    //function that controls the flow of the game of life, calling for the update of both the model and the view
    //based on the fpsvalue to control the speed of simulation
    gameLoop(){
        setTimeout( () => {
            if(this.running){
                this.gol_grid.nextAge();
                this.interface.redraw(this.gol_grid.cells);
                window.requestAnimationFrame(() => this.gameLoop());
            }
            
        }, this.interface.fpsvalue)
    }
    

    

    

}



//VIEW, add the logic to make the data passed by the CONTROLLER be visualized correctly



class View {
    constructor(rows,cols){

        // #of rows and columns
        this.rows = rows;
        this.cols = cols;

        //initial scale factor
        this.scalefactor = 1.1;
        

        this.scalex = 1;
        this.scaley = 1;

        this.cellsize = 5;
        this.cellspace = 1;

        this.width = this.cols*this.cellsize + this.cols*this.cellspace;
        this.height = this.rows*this.cellsize + this.rows*this.cellspace;


        this.lastX=0, this.lastY=0;
        this.offsetX=0, this.offsetY=0;
		this.dragStart,this.dragged;

        //elements of the DOM 
        //here i decided to have 2 canvases one on top of the other
        //one is for painting the grid, the other for painting the cells on top of the grid
        this.grid = document.getElementById('gol');
        this.grid_cells = document.getElementById('gol_cells');

        this.grid_ctx = this.grid.getContext('2d');
        this.cell_ctx = this.grid_cells.getContext('2d');

        this.btnstart = document.getElementById('start');
        this.btnclear = document.getElementById('clear');
        this.btnrandom = document.getElementById('random');
        this.zoomin = document.getElementById('zoomin');
        this.zoomout = document.getElementById('zoomout');

        this.fps = document.getElementById('fps');

        //value that controls the simulation speed
        this.fpsvalue = this.fps.value;



        this.grid.width = this.width;
        this.grid.height =this.height;
        this.grid.style.height = "600px";

        this.grid_cells.width = this.width;
        this.grid_cells.height =this.height;
        this.grid_cells.style.height = "600px";
        this.initialscale = this.width/600;
        this.grid_ctx.scale(this.initialscale, this.initialscale);
        this.cell_ctx.scale(this.initialscale, this.initialscale);
        this.offsetX = -this.width/(2*this.initialscale);
        this.offsetY = -this.height/(2*this.initialscale);

        this.offsetX += 600/(2*this.initialscale);
        this.offsetY += 600/(2*this.initialscale);

        this.grid_ctx.fillStyle = 'white';
        this.grid_ctx.fillRect(0,0,this.width,this.height);

        //colors used to paint differently the cells of the game of life, based on how old they are
        this.colors = ["rgb(1, 0, 255)","rgb(1, 95, 255)","rgb(1, 185, 255)","rgb(1, 219, 255)",
                          "rgb(186, 0, 255)",
                        "rgb(185, 0, 132)", "rgb(255, 87, 0)", "rgb(255, 49, 0)", "rgb(255, 3, 0)","rgb(255, 0, 0)"
                    ]

        this.cell_ctx.fillStyle = 'transparent';
        this.cell_ctx.fillRect(0,0,this.width,this.height);
        
    }

    //function used to transform coordinates
    grid_to_screen(gridX, gridY){
        var screenX = (-gridX+this.offsetX)*this.scalex*this.initialscale;
        var screenY = (-gridY+this.offsetY)*this.scaley*this.initialscale;
        return [screenX, screenY];
    }

    //function used to transform coordinates
    screen_to_grid(screenX, screenY){
        var gridX = ((screenX/this.scalex/this.initialscale)-this.offsetX*this.scalex*this.initialscale);
        var gridY = ((screenY/this.scaley/this.initialscale)-this.offsetY*this.scaley*this.initialscale);
        return [gridX, gridY];
    }

    //calls for draw grid and redraw cells to update the canvases
    redraw(cells){
        var p1 = this.grid_to_screen(0,0);
        var p2 = this.grid_to_screen(this.offsetX,this.offsetY);
        

        this.grid_ctx.setTransform(this.initialscale, 0, 0, this.initialscale, 0, 0);
        this.cell_ctx.setTransform(this.initialscale, 0, 0, this.initialscale, 0, 0);

        this.grid_ctx.clearRect(0,0,this.grid.width,this.grid.height);
        
        
        this.cell_ctx.clearRect(0,0,this.grid.width,this.grid.height);

        
        this.grid_ctx.scale(this.scalex, this.scaley);
        this.cell_ctx.scale(this.scalex, this.scaley);
        this.draw_grid(p1[0], p1[1]);
        this.redraw_cells(cells, p1[0]+p2[0], p1[1]+p2[1]);
    }

    //draw the grid of the game of life
    draw_grid(x,y){
        for(var i=0;i<this.cols;i++){
            this.grid_ctx.strokeStyle = 'black';
            this.grid_ctx.beginPath();
            this.grid_ctx.moveTo(x + (this.cellspace*i) + (this.cellsize*i), y + 0);
            this.grid_ctx.lineTo(x + (this.cellspace*i) + (this.cellsize*i), y + this.height);
            this.grid_ctx.stroke();
            //this.grid_ctx.strokeRect(this.cellspace + (this.cellspace*i) + (this.cellsize*i), 0, this.cellsize, this.height);
            
        }
        for(var i=0;i<this.rows;i++){
            this.grid_ctx.strokeStyle = 'black';
            this.grid_ctx.beginPath();
            this.grid_ctx.moveTo(x, y + (this.cellspace*i) + (this.cellsize*i));
            this.grid_ctx.lineTo(x + this.width, y + (this.cellspace*i) + (this.cellsize*i));
            this.grid_ctx.stroke();
        }
    }

        
    redraw_cells(c,x,y){
        for(var i=0;i<this.cols;i++){
            for(var j=0;j<this.rows;j++){
                if(c[i][j]){
                    this.draw_cell(i,j,c[i][j],x,y);
                }
            }
        }
    }

    //draw cell in position i,j
    draw_cell(i,j,a=0,x,y){
        if(a){
            //se alive
            this.cell_ctx.fillStyle = this.colors[a];
            this.cell_ctx.fillRect(x + (this.cellspace*i) + (this.cellsize*i), y + (this.cellspace*j) + (this.cellsize*j), this.cellsize+1, this.cellsize+1);
            
        }else{
            //dead
            this.cell_ctx.fillStyle = 'transparent';
            this.cell_ctx.clearRect(x + (this.cellspace*i) + (this.cellsize*i), y + (this.cellspace*j) + (this.cellsize*j), this.cellsize+1, this.cellsize+1);
        }
    }

    //method called to update the speed of the simulation
    update_fps(){
        this.fpsvalue = this.fps.value;
    }
    

    //Here we have to listener to all the events that can arise from the interface...
    //Only catches the events, the handler and how to react to an event is defined in the controller, with an handler
    //for every type of event...
    bindMouseDown(handler){
        this.grid_cells.addEventListener('mousedown', event => {
            handler(event)
        }, false);
    }


    bindMouseMove(handler){
        this.grid_cells.addEventListener('mousemove', event => {
            handler(event)
        }, false);
    }

    bindMouseUp(handler){
        this.grid_cells.addEventListener('mouseup', event => {
            handler(event)
        }, false);
    }

    bindDOMMouseScroll(handler){
        this.grid_cells.addEventListener('DOMMouseScroll', event => {
            handler(event)
        }, false);
    }


    bindMouseWheel(handler){
        this.grid_cells.addEventListener('mousewheel', event => {
            handler(event)
        }, false);
    }

    bindStartClick(handler){
        this.btnstart.addEventListener('click', event => {
            handler(event)
        }, false);
    }


    bindRandomClick(handler){
        this.btnrandom.addEventListener('click', event => {
            handler(event)
        }, false);
    }


    bindClearClick(handler){
        this.btnclear.addEventListener('click', event => {
            handler(event)
        }, false);
    }


    rangeListener(handler){
        this.fps.addEventListener('mouseup', event =>{
            handler(event);
        }, false);
        this.fps.addEventListener('mousemove', event =>{
            handler(event);
        }, false);
    }



    

}


const control = new Controller();

