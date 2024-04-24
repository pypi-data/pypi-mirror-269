import os
from dotenv import load_dotenv


def load_envfile():
  # Obtener el nombre del archivo de entorno de los argumentos de la línea de comandos
  env_file = None
  if "--env-file" in sys.argv:
      index = sys.argv.index("--env-file")
      if index + 1 < len(sys.argv):
          env_file = sys.argv[index + 1]

  # Cargar las variables de entorno desde el archivo especificado
  if env_file:
      load_dotenv(env_file)