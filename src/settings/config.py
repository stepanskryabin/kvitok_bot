from dotenv import dotenv_values

get_env = dotenv_values(".env")

TELEGRAM_TOKEN = get_env["TELEGRAM_TOKEN"]
LOGIN = get_env["LOGIN"]
PASSWORD = get_env["PASSWORD"]
BROWSER_DRIVER = get_env["BROWSER_DRIVER"]
BROWSER_TIME = get_env["BROWSER_TIME"]
URL = get_env["URL"]
