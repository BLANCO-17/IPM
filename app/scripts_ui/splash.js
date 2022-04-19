const {ipcRenderer} = require('electron');

function check_startup(count){
    fetch('http://127.0.0.1:5000/fromapp')
    .then(data => data.text())
    .then((data) =>  {
        data = JSON.parse(data);
        if(data.status == 200) 
        {
            console.log("Backend Loaded Successfully.");
            ipcRenderer.send("START_APP");
            return;
        }
        return;
    }).catch(error =>{

        if(count < 5){
            console.log(count);
            setTimeout(check_startup(count+1), 3000);
        }
        else{
            ipcRenderer.send("FALSE_START");
            console.log("cut it out.");
        }
        
    });
}

window.onload = function() {
    
    // let counter = 0;
    check_startup(0);
}