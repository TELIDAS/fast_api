from decouple import config

DB_URI = config("DB_URI")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
