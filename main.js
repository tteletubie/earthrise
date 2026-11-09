const { app, BrowserWindow, Menu } = require('electron');
const path = require('node:path');

Menu.setApplicationMenu(null);

const createWindow = () => {
  const window = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 320,
    minHeight: 240,
    backgroundColor: '#f5f5f5',
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  window.setMenu(null);

  // Load the fonts in each view (@font-face in CSS fails in Electron)
  window.webContents.on('dom-ready', () => {
    window.webContents.executeJavaScript(`
      ['400', '600', '700'].forEach((weight) => {
        new FontFace('Source Sans 3', 'url(fonts/source-sans-3-' + weight + '.ttf)', { weight })
          .load()
          .then((font) => document.fonts.add(font))
          .catch((error) => console.error('Font error', weight, error));
      });
    `);
  });

  window.loadFile(path.join(__dirname, 'views', 'home', 'home.html'));
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