import os
import web
from mvc.models.model_contactos import ModelContactos

render = web.template.render('mvc/views', base='template')

class InsertarContacto:

    # Renderiza el arhivo insertar_contacto.html
    def GET(self):
        return render.insertar_contacto()
    
    # Recibe los input del formulario y accede a cada uno
    # utilizando el atributo 'name'
    def POST(self):
        # Accede a los datos del formulario 'contactos'
        formulario = web.input(foto={})
        # Obtiene el valor del input del nombre
        nombre = formulario['nombre']
        # Obtiene el valor del input del email
        email = formulario['email']
        # Obtiene el valor del input del telefono
        telefono = formulario['telefono']
        
        archivo = formulario['foto']
        foto = archivo.filename
        
        ruta = os.path.join("static/fotos/", foto)
        with open(ruta, "wb") as file:
            file.write(formulario.foto.file.read())

        # Imprime los datos para verificar que se obtienen los valores de forma correcta.
        # print(f"Nombre: {nombre}")
        # print(f"Email: {email}")
        # print(f"Teléfono: {telefono}")
        
        #contenido_bytes = archivo.file.read()

        model_contactos = ModelContactos()
        datos = model_contactos.insertarContacto(nombre, email, telefono, foto)

        #print (datos)

        web.header('Content-Type', 'text/html')
        html = "<h1>Contacto almacenado correctamente</h1> <a href='/contactos'>Regresar</a>"

        return html