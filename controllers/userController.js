const { ipcMain } = require('electron');
const UserModel = require('../models/userModel');

function registerUserController() {
  ipcMain.handle('usuario:create', async (event, payload) => {
    try {
      const nombre = payload?.nombre?.trim();
      const apellido_paterno = payload?.apellido_paterno?.trim();
      const id_grado = Number(payload?.id_grado);

      if (!nombre || !apellido_paterno || !id_grado) {
        throw new Error('Todos los campos son obligatorios.');
      }

      const usuario = UserModel.create({ nombre, apellido_paterno, id_grado });
      return { success: true, data: usuario };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  ipcMain.handle('usuario:getActive', async () => {
    try {
      const usuario = UserModel.getActiveTeacher();
      return { success: true, data: usuario || null };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });
}

module.exports = registerUserController;
