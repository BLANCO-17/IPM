const { app, ipcMain } = require('electron');
const  {BrowserWindow } = require('electron-acrylic-window')

function createWindow() {
    const win = new BrowserWindow({
        minWidth: 600,
        minHeight: 500,
        title: "IPM",
        frame: false,
        transparent: true,
        webPreferences: {nodeIntegration: true,  enableRemoteModule: true, contextIsolation: false}
    });

    win.setSize(1280, 768);
    win.loadFile('index.html');
    win.webContents.openDevTools();

    op = {
        theme: 'dark',
        effect: 'blur',
        useCustomWindowRefreshMethod: true,
        maximumRefreshRate: 60,
        disableOnBlur: false
    };

    win.setVibrancy(op);

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
    
};

app.whenReady().then(()=>{
    createWindow();
});