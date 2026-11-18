import os
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import hmac

import logging


load_dotenv()

logger = logging.getLogger(__name__)

class ModelContactos:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL" , ""),
                os.environ.get("SUPABASE_KEY" , "")
            )
            self.SECRET_KEY = b"adios"
        except Exception as error:
            logger.error(f"ERROR 100: {str(error)}")
            print(f"ERROR 100: {error.args[0]}")

    def generar_hash(self, id: int) -> str:
        try:
            """Genera un hash único a partir del ID."""
            mensaje = str(id).encode("utf-8")
            firma = hmac.new(self.SECRET_KEY, mensaje, hashlib.sha256).hexdigest()
            # Concatena el id:firma
            return f"{id}:{firma}"
        except Exception as error:
            logger.error(f"ERROR 106: {str(error)}")
            print(f"ERROR 106: {error.args[0]}")
            return ""

    def validar_hash(self, hash_a_validar: str) -> int | None:
        try:
            id_str, sep, _ = hash_a_validar.partition(":")
            if sep and id_str.isdigit():
                token_esperado = self.generar_hash(int(id_str))
                if hmac.compare_digest(token_esperado, hash_a_validar):
                    return int(id_str)
            return None
        except Exception as error:
            logger.error(f"ERROR 107: {str(error)}")
            print(f"ERROR 107: {error.args[0]}")
            return None

    def obtenerContactos(self):
        # SELECT * FROM contactos;
        try: 
            response = self.supabase.table("contactos").select("*").execute()
            for registro in response.data:
                registro["id_contacto"] = self.generar_hash(int(registro["id_contacto"]))
            return response.data
        except Exception as error:
            logger.error(f"ERROR 101: {str(error)}")
            print(f"ERROR 101: {error.args[0]}")

    def buscarContacto(self, id_contacto:str):

        try: 
            id = self.validar_hash(id_contacto)
            if id is None:
                return []
            response = self.supabase.table("contactos").select("*").eq("id_contacto", id).execute()
            for registro in response.data:
                registro["id_contacto"] = self.generar_hash(int(registro["id_contacto"]))
            return response.data
        except Exception as error:
            logger.error(f"ERROR 102: {str(error)}")
            print(f"ERROR 102: {error.args[0]}")
            return []


    def insertarContacto(self, nombre:str, email:str, telefono:str, foto:str):
        try:
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "foto": foto
            }
            response = self.supabase.table("contactos").insert(data).execute()
            return response.data
        except Exception as error:
            logger.error(f"ERROR 103: {str(error)}")
            print(f"ERROR 103: {error.args[0]}")

    def borrarContacto(self, id_contacto:str):
        try:
            id = self.validar_hash(id_contacto)
            if id is None:
                return []
            response = self.supabase.table("contactos").delete().eq("id_contacto", id).execute()
            return response.data
        except Exception as error:
            logger.error(f"ERROR 104: {str(error)}")
            print(f"ERROR 104: {error.args[0]}")

    def actualizarContacto(self, id_contacto:str, nombre:str, email:str, telefono:str, foto:str):
        try:
            id = self.validar_hash(id_contacto)
            if id is None:
                return []
            valores_nuevos = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "foto": foto
            }
            response = self.supabase.table("contactos").update(valores_nuevos).eq("id_contacto", id).execute()
            return response.data

        except Exception as error:
            logger.error(f"ERROR 105: {str(error)}")
            print(f"ERROR 105: {error.args[0]}")

if __name__ == "__main__":
    model_contactos = ModelContactos()
    contactos = model_contactos.obtenerContactos()
    print(contactos)
    print(model_contactos.buscarContacto(contactos[0]["id_contacto"]))
    # print(model_contactos.insertarContacto("hola", "hola@gmail.com", "2222", "foto.jpg"))
    # print(model_contactos.borrarContacto(contactos[0]["id_contacto"]))
    # print(model_contactos.actualizarContacto(contactos[0]["id_contacto"], "Dejah modificada", "dejah11@gmail.com", "444444", "foto.jpg"))