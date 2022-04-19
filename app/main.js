const { app, ipcMain, dialog } = require('electron');
const  {BrowserWindow } = require('electron-acrylic-window')

async function createWindow() {
    const win = new BrowserWindow({
        minWidth: 1280,
        minHeight: 720,
        title: "IPM",
        frame: false,
        show: false,
        webPreferences: {nodeIntegration: true,  enableRemoteModule: true, contextIsolation: false}
    });

    win.setSize(1280, 768);
    // win.loadFile('index.html');
    // win.webContents.openDevTools();

    op = {
        theme: 'light',
        effect: 'blur',
        useCustomWindowRefreshMethod: true,
        maximumRefreshRate: 60,
        disableOnBlur: false
    };

    win.setVibrancy(op);

    var splash = new BrowserWindow({
        width: 500, 
        height: 300, 
        transparent: true, 
        frame: false, 
        alwaysOnTop: true,
        webPreferences: {nodeIntegration: true,  enableRemoteModule: true, contextIsolation: false}
    });

    // splash.webContents.openDevTools();
    splash.loadFile('splash.html');
    splash.center();         

    ipcMain.on('close-win', ()=>{
        win.close()
        app.quit()
    });
    ipcMain.on('max-win', ()=>{
        win.isMaximized() ? win.unmaximize() : win.maximize()
    });
    ipcMain.on('min-win', ()=>{
        win.minimize();
    });

    ipcMain.on('FALSE_START', () => {

        console.log("bruh")
        // dialog.showErrorBox("FAILED TO START APP", "ERROR[FALSE_START] - 0x0001");
        dialog.showMessageBoxSync(splash, {
            title: "FAILED TO START APP",
            message: "ERROR[ FALSE_START ] - 0x0001",
            type: "error"
        });
        win.close();
        splash.close();
        app.quit();
    });
    
    ipcMain.on('START_APP', ()=>{

        win.loadFile('index.html')
        win.center()
        setTimeout(function () {
            splash.close();
            win.show();
        }, 6000);
    });
    
};

app.whenReady().then(()=>{
    createWindow();
});