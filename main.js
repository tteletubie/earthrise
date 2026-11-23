const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const path = require('node:path');
const fs = require('node:fs');
const nunjucks = require('nunjucks');
const registerUserController = require('./controllers/userController');
const UserModel = require('./models/userModel');

Menu.setApplicationMenu(null);

const viewsRoot = path.join(__dirname, 'views');
const allowedTemplates = new Set([
  'home/home.njk'
]);

const nunjucksEnvironment = nunjucks.configure(viewsRoot, { autoescape: true });

function verifyTemplates() {
  for (const templateName of allowedTemplates) {
    const templatePath = path.join(viewsRoot, templateName);
    if (!fs.existsSync(templatePath)) {
      throw new Error(`The permitted template is missing.: ${templateName}`);
    }
    nunjucksEnvironment.getTemplate(templateName, true);
  }
}

ipcMain.handle('templates:render', async (event, templateName) => {
  try {
    if (typeof templateName !== 'string') {
      throw new Error('The template name must be a string.');
    }
    if (!allowedTemplates.has(templateName)) {
      throw new Error('Template not permitted.');
    }

    const activeUser = UserModel.getActiveTeacher();
    const html = nunjucks.render(templateName, { usuario: activeUser || null });
    return { success: true, html };
  } catch (error) {
    return { success: false, error: error.message || 'The template could not be rendered.' };
  }
});

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
      nodeIntegration: false,
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  window.setMenu(null);
  window.loadFile(path.join(__dirname, 'index.html'));
};

app.whenReady().then(() => {
  verifyTemplates();
  registerUserController();
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