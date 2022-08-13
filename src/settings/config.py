from dotenv import dotenv_values

get_env = dotenv_values(".env")

TELEGRAM_TOKEN = get_env["TELEGRAM_TOKEN"]
LOGIN = get_env["LOGIN"]
PASSWORD = get_env["PASSWORD"]
USER_AGENT = get_env["USER_AGENT"]
URL_ZYNOVY = get_env["URL_ZYNOVY"]
URL_UKCH = get_env["URL_UKCH"]
URL_UKB = get_env["URL_UKB"]
