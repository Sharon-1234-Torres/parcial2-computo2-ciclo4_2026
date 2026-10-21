import hashlib
import re
import conexion

db = conexion.Conexion()
TABLA = "usuarios_usss096224"


def encriptar(clave):
    # md5 = 32 caracteres, cabe en char(35)
    return hashlib.md5(clave.encode("utf-8")).hexdigest()


class crud_usuarios_usss096224:
    def consultar(self, buscar):
        like = f"%{buscar}%"
        return db.consultar(
            f"SELECT idUsuario, usuario, nombre, direccion, telefono FROM {TABLA} "
            "WHERE usuario LIKE %s OR nombre LIKE %s OR telefono LIKE %s ORDER BY nombre",
            (like, like, like))

    def login(self, usuario, clave):
        filas = db.consultar(
            f"SELECT idUsuario, usuario, nombre FROM {TABLA} WHERE usuario=%s AND clave=%s",
            (usuario, encriptar(clave)))
        return filas[0] if filas else None

    def validar(self, d, requiere_clave):
        if not re.fullmatch(r"[A-Za-z0-9_.]{3,35}", d.get('usuario', '')):
            return "Usuario invalido (3-35 letras, numeros, _ o .)"
        if requiere_clave and not (4 <= len(d.get('clave', '')) <= 35):
            return "La clave debe tener entre 4 y 35 caracteres"
        if d.get('clave') and len(d['clave']) > 35:
            return "La clave no puede exceder 35 caracteres"
        if not 3 <= len(d.get('nombre', '').strip()) <= 85:
            return "Nombre invalido (3-85 caracteres)"
        if len(d.get('direccion', '')) > 100:
            return "Direccion demasiado larga (max 100)"
        if not re.fullmatch(r"[0-9]{4}-[0-9]{4}", d.get('telefono', '')):
            return "Telefono invalido, use el formato 0000-0000"
        return None

    def administrar(self, datos):
        accion = datos.get('accion')
        try:
            if accion == 'nuevo':
                error = self.validar(datos, True)
                if error:
                    return error
                sql = (f"INSERT INTO {TABLA}(usuario,clave,nombre,direccion,telefono) "
                       "VALUES(%s,%s,%s,%s,%s)")
                valores = (datos['usuario'], encriptar(datos['clave']), datos['nombre'].strip(),
                           datos['direccion'], datos['telefono'])
            elif accion == 'modificar':
                error = self.validar(datos, False)
                if error:
                    return error
                if datos.get('clave'):  # solo cambia la clave si se escribe una nueva
                    sql = (f"UPDATE {TABLA} SET usuario=%s,clave=%s,nombre=%s,direccion=%s,telefono=%s "
                           "WHERE idUsuario=%s")
                    valores = (datos['usuario'], encriptar(datos['clave']), datos['nombre'].strip(),
                               datos['direccion'], datos['telefono'], datos['idUsuario'])
                else:
                    sql = (f"UPDATE {TABLA} SET usuario=%s,nombre=%s,direccion=%s,telefono=%s "
                           "WHERE idUsuario=%s")
                    valores = (datos['usuario'], datos['nombre'].strip(), datos['direccion'],
                               datos['telefono'], datos['idUsuario'])
            elif accion == 'eliminar':
                sql = f"DELETE FROM {TABLA} WHERE idUsuario=%s"
                valores = (datos['idUsuario'],)
            else:
                return "Accion no valida"
            resp = db.ejecutar(sql, valores)
            if 'Duplicate entry' in resp:
                return "Ese usuario ya existe"
            return resp
        except KeyError as e:
            return f"Falta el dato: {e}"
