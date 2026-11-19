const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  usuario: {
    create: (data) => ipcRenderer.invoke('usuario:create', data),
    getActive: () => ipcRenderer.invoke('usuario:getActive')
  }
});
