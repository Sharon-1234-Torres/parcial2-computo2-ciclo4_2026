from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from http import cookies
import json
import secrets

import crud_usuarios_usss096224

port = 3000
crudUsuarios = crud_usuarios_usss096224.crud_usuarios_usss096224()
sesiones = {}  # token -> datos del usuario


class miServidor(SimpleHTTPRequestHandler):
    def sesion(self):
        c = cookies.SimpleCookie(self.headers.get('Cookie', ''))
        return sesiones.get(c['token'].value) if 'token' in c else None

    def responder_json(self, datos, codigo=200, extra=None):
        self.send_response(codigo)
        self.send_header("Content-type", "application/json; charset=utf-8")
        if extra:
            for k, v in extra:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(json.dumps(datos).encode("utf-8"))

    def enviar_archivo(self, ruta):
        self.path = ruta
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        longitud = int(self.headers.get('Content-Length', 0))
        try:
            datos = json.loads(self.rfile.read(longitud).decode("utf-8"))
        except ValueError:
            return self.responder_json({'msg': 'Datos invalidos'}, 400)

        if datos.get("modulo") == "login":
            user = crudUsuarios.login(datos.get('usuario', ''), datos.get('clave', ''))
            if not user:
                return self.responder_json({'msg': 'Usuario o clave incorrectos, acceso denegado'})
            token = secrets.token_hex(16)
            sesiones[token] = user
            return self.responder_json({'msg': 'ok'}, extra=[
                ('Set-Cookie', f'token={token}; Path=/; HttpOnly; SameSite=Strict')])

        if datos.get("modulo") == "logout":
            c = cookies.SimpleCookie(self.headers.get('Cookie', ''))
            if 'token' in c:
                sesiones.pop(c['token'].value, None)
            return self.responder_json({'msg': 'ok'}, extra=[
                ('Set-Cookie', 'token=; Path=/; Max-Age=0')])

        if not self.sesion():
            return self.responder_json({'msg': 'Acceso denegado, inicie sesion'}, 401)
        if datos.get("modulo") == "usuario":
            return self.responder_json({'msg': crudUsuarios.administrar(datos)})
        self.responder_json({'msg': 'Modulo no valido'}, 400)

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
        ruta = urlParse.path
        user = self.sesion()

        # El login es lo primero que se muestra
        if ruta == "/" or ruta == "/login":
            if user:
                self.send_response(302)
                self.send_header("Location", "/sistema")
                self.end_headers()
                return
            return self.enviar_archivo("/login.html")

        if ruta == "/sistema":
            if not user:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            return self.enviar_archivo("/index.html")

        if not user:  # todo lo demas requiere sesion
            self.send_response(401)
            self.end_headers()
            return

        if ruta == "/sesion":
            return self.responder_json(user)
        if ruta == "/usuarios":
            return self.responder_json(crudUsuarios.consultar(qs.get('buscar', [''])[0]) or [])
        if ruta == "/vistas":
            form = qs.get('form', [''])[0]
            if form in ("usuarios", "busqueda_usuarios"):
                return self.enviar_archivo(f"/modulos/{form}.html")
        if ruta == "/app.js":
            return self.enviar_archivo("/app.js")
        self.send_response(404)
        self.end_headers()


print(f"Servidor corriendo en http://localhost:{port}")
HTTPServer(("localhost", port), miServidor).serve_forever()
