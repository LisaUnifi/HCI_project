//MODEL, a 2 dimensional array that has values 0 if cell is dead, 1 if alive. Must implement
//all the logic to update dinamically the grid and to tell if a cell has the right number of neighbors


class Cell {
    constructor(){
        this.age = 0;
        this.alive = 0;
    }

    get age(){
        return this.age;
    }
    get alive(){
        return this.alive;
    }
    dies(){
        this.age = 0;
        this.alive = 0;
    }
    born(){
        this.alive = 1;
        this.age = 1;
    }
    incrementAge(){
        this.age++;
    }
    //non so se usare questa implementazione, forse appesantisce troppo
}


class Grid {
    constructor(rows, columns){
        this.rows = rows;
        this.columns = columns;
        this.cells = new Array(rows);
        for(var i=0; i<rows;i++){
            this.cells[i] = new Uint8Array(columns);
            for(var j=0;j<columns;j++){
                this.cells[i][j] = 0;
            }
        }
    }

    //create a cell
    createCell(r,c){
        this.cells[r][c] = 1;
        //se fare altre cose, aggiungere altro
    }


    //delete a cell
    deleteCell(r,c){
        this.cells[r][c]=0;
        //se fare altre cose, aggiungere altro
    }


    //create a cell
    switchCell(r,c){
        if(this.cells[r][c]==1){
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
        sum = (this.cells[r-1][c-1] + this.cells[r-1][c] + this.cells[r-1][c+1] + //precedent row
        this.cells[r][c-1] + this.cells[r][c+1] + //current row
        this.cells[r+1][c-1] + this.cells[r+1][c] + this.cells[r+1][c+1]); //successive row
        return sum;
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


    //age of cells? do i implement this?
    nextAge(){
        changed = [];
        k=0;
        for(var i=0;i<this.rows;i++){
            for(var j=0;j<this.columns;j++){
                count = this.countNeighbors(i,j);
                if(count>3 || count<2 && this.cells[i][j]==1){
                    changed[k]=i;
                    changed[k+1]=j;
                    k=k+2;
                }else if(count>1 && count<4 && this.cells[i][j]==0){
                    changed[k]=i;
                    changed[k+1]=j;
                    k=k+2;
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
        this.rows = 100;
        this.cols = 100;
        this.gol_grid = new Grid(this.rows,this.cols);
        this.interface = new View(this.rows,this.cols);
        this.bindHandlers();
        this.interface.trackTransforms(this.interface.grid_ctx);
        this.interface.trackTransforms(this.interface.cell_ctx);
    }

    bindHandlers(){
        this.interface.bindZoomInClick(this.zoominClickHandler);
        this.interface.bindMouseDown(this.mouseDownHandler);
        this.interface.bindMouseMove(this.mouseMoveHandler);
        this.interface.bindMouseUp(this.mouseUpHandler);
        this.interface.bindDOMMouseScroll(this.scrollHandler);
        this.interface.bindMouseWheel(this.scrollHandler);
    }


    //user inputs must be controlled here

    //used when click happens inside the canvas. Returns the x and y of the cell clicked
    
    canvasClickHandler = (e) => {
        var pos = this.mousePos(e);
        if(pos[0]){
            var alive = this.gol_grid.switchCell(pos[1],pos[2]);
            //colorare quadratino
            this.interface.draw_cell(pos[1],pos[2],alive);
        }
        
        
    }


    mousePos(e){
        var x , y, posx, posy, cellsize=(this.interface.cellsize+1);
        var offsetX = this.interface.offsetX;
        var offsetY = this.interface.offsetY;
        var rect = this.interface.grid.getBoundingClientRect();
        var scalex = this.interface.zoomscale;
        var scaley = this.interface.zoomscale;
        var event = e;

        posx = (event.clientX - rect.left) / scalex;
        posy = (event.clientY - rect.top) / scaley;
        
        if( (posx >= offsetX && posx <= (offsetX+this.interface.grid.width)) && (posy >= offsetY && posy <= (offsetY+this.interface.grid.height)) ){
            x = Math.ceil(((posx-offsetX)/cellsize) - 1);
            y = Math.ceil(((posy-offsetY)/cellsize) - 1);

            return [true, x, y];
        }else{
            return [false, 0,0];
        }
        

        

    }

    zoominClickHandler = (e) => {
        this.interface.zoomscale = this.interface.zoomscale * 1.25;
        this.interface.grid_ctx.scale(this.interface.zoomscale,this.interface.zoomscale);
    }

    
    mouseDownHandler = (e) => {
        document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        this.interface.dragStart = this.interface.grid_ctx.transformedPoint(this.interface.lastX,this.interface.lastY);
        this.interface.dragged = false;
    }


    mouseMoveHandler = (e) => {
        this.interface.lastX = e.offsetX || (e.pageX - this.interface.grid.offsetLeft);
        this.interface.lastY = e.offsetY || (e.pageY - this.interface.grid.offsetTop);
        this.interface.dragged = true;  
        if (this.interface.dragStart){
            var pt = this.interface.grid_ctx.transformedPoint(this.interface.lastX,this.interface.lastY);
            this.interface.grid_ctx.translate(pt.x-this.interface.dragStart.x,pt.y-this.interface.dragStart.y);
            this.interface.cell_ctx.translate(pt.x-this.interface.dragStart.x,pt.y-this.interface.dragStart.y);
            this.interface.offsetX= this.interface.offsetX + pt.x - this.interface.dragStart.x;
            this.interface.offsetY= this.interface.offsetY + pt.y-this.interface.dragStart.y;
            this.interface.redraw(this.gol_grid.cells);
        }
    }

    

    mouseUpHandler = (e) => {
        this.interface.dragStart = null;
        if (!this.interface.dragged) this.canvasClickHandler(e);
    }


    scrollHandler = (e) => {
        var delta = e.wheelDelta ? e.wheelDelta/40 : e.detail ? -e.detail : 0;
        if (delta) this.zoom(delta);
        return e.preventDefault() && false;
    }

    zoom(clicks){
        var pt = this.interface.grid_ctx.transformedPoint(this.interface.lastX, this.interface.lastY);
        var gp = this.interface.grid_ctx.transformedPoint(this.interface.offsetX, this.interface.offsetY);

        var factor = Math.pow(this.interface.scalefactor,clicks);

        this.interface.grid_ctx.translate(pt.x,pt.y);
        this.interface.cell_ctx.translate(pt.x,pt.y);

        this.interface.grid_ctx.scale(factor,factor);
        this.interface.grid_ctx.translate(-pt.x,-pt.y);
        this.interface.cell_ctx.scale(factor,factor);
        this.interface.cell_ctx.translate(-pt.x,-pt.y);


        this.interface.zoomscale = this.interface.zoomscale*factor;
        this.interface.offsetX = gp.x;
        this.interface.offsetY = gp.y;

        this.interface.redraw(this.gol_grid.cells);
    }

    

    

}



//VIEW, add the logic to make the data passed by the CONTROLLER be visualized correctly

let MAX_ZOOM = 5;
let MIN_ZOOM = 0.1;

class View {
    constructor(rows,cols){

        this.rows = rows;
        this.cols = cols;

        this.scalefactor = 1.1;

        this.zoomscale = 1;

        this.cellsize = 5;
        this.cellspace = 1;

        this.width = this.cols*this.cellsize + this.cols*this.cellspace;
        this.height = this.rows*this.cellsize + this.rows*this.cellspace;


        this.lastX=0, this.lastY=0;
        this.offsetX=0, this.offsetY=0;
		this.dragStart,this.dragged;


        this.grid = document.getElementById('gol');
        this.grid_cells = document.getElementById('gol_cells');

        this.grid_ctx = this.grid.getContext('2d');
        this.cell_ctx = this.grid_cells.getContext('2d');

        this.btnstart = document.getElementById('start');
        this.btnclear = document.getElementById('clear');
        this.btnrandom = document.getElementById('random');
        this.zoomin = document.getElementById('zoomin');
        this.zoomout = document.getElementById('zoomout');



        this.grid.width = this.width;
        this.grid.height =this.height;
        this.grid.style.width = String(this.width)+"px";
        this.grid.style.height =String(this.height)+"px";

        this.grid_cells.width = this.width;
        this.grid_cells.height =this.height;
        this.grid_cells.style.width = String(this.width)+"px";
        this.grid_cells.style.height =String(this.height)+"px";
        //inizializzo colore canvas backgroudn
        this.grid_ctx.fillStyle = 'white';
        this.grid_ctx.fillRect(0,0,this.width,this.height);

        this.cell_ctx.fillStyle = 'transparent';
        this.cell_ctx.fillRect(0,0,this.width,this.height);

        //inizializzo la griglia
        this.initialize_grid();
        
    }

    grid_to_screen(gridX, gridY){
        var screenX = (gridX-this.offsetX);
        var screenY = (gridY-this.offsetY);
        return [screenX, screenY];
    }


    screen_to_grid(screenX, screenY){
        var gridX = (screenX-this.offsetX);
        var gridY = (screenY-this.offsetY);
        return [gridX, gridY];
    }


    redraw(cells){
        var p1 = this.grid_ctx.transformedPoint(0,0);
        var p2 = this.grid_ctx.transformedPoint(this.grid.width,this.grid.height);
        this.grid_ctx.clearRect(p1.x,p1.y,p2.x-p1.x,p2.y-p1.y);
        this.draw_grid();
        var p1 = this.cell_ctx.transformedPoint(0,0);
        var p2 = this.cell_ctx.transformedPoint(this.grid_cells.width,this.grid_cells.height);
        this.cell_ctx.clearRect(p1.x,p1.y,p2.x-p1.x,p2.y-p1.y);
        this.redraw_cells(cells);
    }

    draw_grid(){
        for(var i=0;i<this.cols;i++){
            this.grid_ctx.strokeStyle = 'black';
            this.grid_ctx.beginPath();
            this.grid_ctx.moveTo((this.cellspace*i) + (this.cellsize*i),0);
            this.grid_ctx.lineTo((this.cellspace*i) + (this.cellsize*i), this.height);
            this.grid_ctx.stroke();
            //this.grid_ctx.strokeRect(this.cellspace + (this.cellspace*i) + (this.cellsize*i), 0, this.cellsize, this.height);
            
        }
        for(var i=0;i<this.rows;i++){
            this.grid_ctx.strokeStyle = 'black';
            this.grid_ctx.beginPath();
            this.grid_ctx.moveTo(0,(this.cellspace*i) + (this.cellsize*i));
            this.grid_ctx.lineTo(this.width,(this.cellspace*i) + (this.cellsize*i));
            this.grid_ctx.stroke();
        }
    }


    initialize_grid(){
        this.draw_grid();
    }

    
    redraw_cells(c){
        for(var i=0;i<this.cols;i++){
            for(var j=0;j<this.rows;j++){
                if(c[i][j]){
                    this.draw_cell(i,j,c[i][j]);
                }
            }
        }
    }


    draw_cell(i,j,a=0){
        if(a){
            //se alive
            this.cell_ctx.fillStyle = 'black';
            this.cell_ctx.fillRect((this.cellspace*i) + (this.cellsize*i), (this.cellspace*j) + (this.cellsize*j), this.cellsize+1, this.cellsize+1);
        }else{
            //dead
            this.cell_ctx.clearRect((this.cellspace*i) + (this.cellsize*i), (this.cellspace*j) + (this.cellsize*j), this.cellsize+1, this.cellsize+1);
        }
    }
    

    bindZoomInClick(handler){
        this.zoomin.addEventListener('click', event => {
            handler(event)
        }, false);
    }


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


    /*
    zoom = function(clicks){
        var pt = this.grid_ctx.transformedPoint(this.lastX,this.lastY);
        this.grid_ctx.translate(pt.x,pt.y);
        var factor = Math.pow(this.scaleFactor,clicks);
        this.grid_ctx.scale(factor,factor);
        this.grid_ctx.translate(-pt.x,-pt.y);
        //this.redraw(); don't do this here
    }
    */

    trackTransforms(ctx){
		var svg = document.createElementNS("http://www.w3.org/2000/svg",'svg');
		var xform = svg.createSVGMatrix();
		ctx.getTransform = function(){ return xform; };
		
		var savedTransforms = [];
		var save = ctx.save;
		ctx.save = function(){
			savedTransforms.push(xform.translate(0,0));
			return save.call(ctx);
		};
		var restore = ctx.restore;
		ctx.restore = function(){
			xform = savedTransforms.pop();
			return restore.call(ctx);
		};

		var scale = ctx.scale;
		ctx.scale = function(sx,sy){
			xform = xform.scaleNonUniform(sx,sy);
			return scale.call(ctx,sx,sy);
		};
		var rotate = ctx.rotate;
		ctx.rotate = function(radians){
			xform = xform.rotate(radians*180/Math.PI);
			return rotate.call(ctx,radians);
		};
		var translate = ctx.translate;
		ctx.translate = function(dx,dy){
			xform = xform.translate(dx,dy);
			return translate.call(ctx,dx,dy);
		};
		var transform = ctx.transform;
		ctx.transform = function(a,b,c,d,e,f){
			var m2 = svg.createSVGMatrix();
			m2.a=a; m2.b=b; m2.c=c; m2.d=d; m2.e=e; m2.f=f;
			xform = xform.multiply(m2);
			return transform.call(ctx,a,b,c,d,e,f);
		};
		var setTransform = ctx.setTransform;
		ctx.setTransform = function(a,b,c,d,e,f){
			xform.a = a;
			xform.b = b;
			xform.c = c;
			xform.d = d;
			xform.e = e;
			xform.f = f;
			return setTransform.call(ctx,a,b,c,d,e,f);
		};
		var pt  = svg.createSVGPoint();
		ctx.transformedPoint = function(x,y){
			pt.x=x; pt.y=y;
			return pt.matrixTransform(xform.inverse());
		}

        
	}

    

}

const control = new Controller();