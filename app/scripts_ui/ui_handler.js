const {ipcRenderer} = require('electron');

let dash_con = true;
let Port_con = false;
let Trad_con = false;

function display_Port(){
    if(!Port_con){

        Port_con = true;        

        let dash = document.getElementById('home_con');
        let port = document.getElementById('port_con');
        let trad = document.getElementById('trad_con');

        document.getElementById('port_btn').style.borderRight = "solid #ec7b39 4px";
        
        if(Trad_con)
        {
            trad.classList.toggle('active');
        }
        else{
            dash.classList.toggle('active');
        }
        dash_con = false;
        Trad_con = false;

        setTimeout(function(){
            document.getElementById('dash_btn').style.borderRight = "none";
            document.getElementById('trad_btn').style.borderRight = "none";
            port.classList.toggle('active');
        }, 500);
    }
}

function display_Dash(){
    if(!dash_con){

        dash_con = true;        

        let dash = document.getElementById('home_con');
        let port = document.getElementById('port_con');
        let trad = document.getElementById('trad_con');


        document.getElementById('dash_btn').style.borderRight = "solid #ec7b39 4px";        

        if(Trad_con)
        {
            trad.classList.toggle('active');
        }
        else{
            port.classList.toggle('active');
        }

        Port_con = false;
        Trad_con = false;

        setTimeout(function(){
            document.getElementById('port_btn').style.borderRight = "none";            
            document.getElementById('trad_btn').style.borderRight = "none";            
            dash.classList.toggle('active');
        }, 500);
    }
}

function display_Trades(){
    if(!Trad_con){

        Trad_con = true;        

        let dash = document.getElementById('home_con');
        let port = document.getElementById('port_con');
        let trad = document.getElementById('trad_con');

        document.getElementById('trad_btn').style.borderRight = "solid #ec7b39 4px";        

        if(Port_con)
        {
            port.classList.toggle('active');
        }
        else{
            dash.classList.toggle('active');
        }
        Port_con = false;
        dash_con = false;
        
        setTimeout(function(){
            document.getElementById('port_btn').style.borderRight = "none";
            document.getElementById('dash_btn').style.borderRight = "none";
            trad.classList.toggle('active');
        }, 500);
    }
}

function toggle_addWindow(){
    document.getElementById('addWindow').classList.toggle('active');
}

function set_graphs(){
    
}

deg=0
function rotate_icons(){
    // console.log('rbuh');

    try{
        var item = document.getElementById("img_rot");
        item.style.webkitTransform = "rotate("+deg+"deg";
        deg+=0.3;
        if(deg > 359.0){
            deg = 1.0;
        }        
    } catch (error) {
        // console.log(deg);        
    }
}


window.onload = function(){

    // document.getElementById('home_con').classList.toggle('active');
    document.getElementById('dash_btn').style.borderRight = "solid #ec7b39 4px";    

    //sidebar  
    let btn = document.getElementById('sidebar_btn');
    btn.onclick = function (){
        document.getElementById('sidebar').classList.toggle('active');
        let textlist = document.getElementsByClassName('text');
        
        for(var i=0; i<textlist.length; i++){
            textlist[i].classList.toggle('active');
        }    
    };        

    // Window events
    let cbtn = document.getElementById('close_btn');
    cbtn.onclick = function winClose(){
        ipcRenderer.send('close-win');
    }

    let maxbtn = document.getElementById('max_btn');
    maxbtn.onclick = function winMax(){
        ipcRenderer.send('max-win');
    };

    let minbtn = document.getElementById('min_btn');
    minbtn.onclick = function winMin(){
        ipcRenderer.send('min-win');
    };    

}; 