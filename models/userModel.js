const db = require('../database/connection');

class UserModel {
  static create({ nombre, apellido_paterno, id_grado }) {
    const stmt = db.prepare(`INSERT INTO usuario (nombre, apellido_paterno, id_grado) VALUES (?, ?, ?)`);
    const info = stmt.run(nombre, apellido_paterno, id_grado);
    console.log('Usuario creado:', { id_usuario: info.lastInsertRowid, nombre, apellido_paterno, id_grado });
    return { id_usuario: info.lastInsertRowid, nombre, apellido_paterno, id_grado };
  }

  static getActiveTeacher() {
    const stmt = db.prepare(`SELECT u.*, g.nombre AS grado_nombre FROM usuario u JOIN grado g ON u.id_grado = g.id_grado ORDER BY u.id_usuario DESC LIMIT 1 `);
    return stmt.get();
  }
}

module.exports = UserModel;
