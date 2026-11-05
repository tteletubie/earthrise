const { app, BrowserWindow } = require('electron');
const path = require('node:path');

const createWindow = () => {
  const window = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 320,
    minHeight: 240,
    backgroundColor: '#f5f5f5',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  window.loadFile(path.join(__dirname, 'views', 'home.html'));
};

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
