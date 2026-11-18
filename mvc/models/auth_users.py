import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

#Lee las variables de entorno
load_dotenv()

#Configura el sistema de logging
logger = logging.getLogger(__name__)

class AuthUsers:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL" , ""),
                os.environ.get("SUPABASE_KEY" , "")
            )
        except Exception as error:
            logger.error(f"ERROR 100: {str(error)}")
            print(f"ERROR 100: {error.args[0]}")

    def iniciarSesion(self, email:str, password:str):
        try:
            response = self.supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
            # print(f"Inicio de sesión exitoso: {response.session.access_token}")
            return response.session.access_token # type: ignore
        except Exception as error:
            logger.error(f"ERROR 101: {str(error)}")
            print(f"ERROR 101: {error.args[0]}")
            return None

    def registrarUsuario(self, email:str, password:str) -> str:
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
            print("Usuario registrado exitosamente")
            return response.user.id # type: ignore

        except Exception as error:
            logger.error(f"ERROR 102: {str(error)}")
            print(f"ERROR 102: {error.args[0]}")
            return None

if __name__ == "__main__":
    print("Autenticación de usuarios")
    objeto = AuthUsers()
    print(objeto.iniciarSesion("dejah@email.com", "123456789")) # Contraseña no valida
    print(objeto.iniciarSesion("dejah@email.com", "12345678")) # Contraseña valida

    print(objeto.registrarUsuario("john@email.com", "12345678"))
