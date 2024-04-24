import requests
from pathlib import Path
import toml
from dotenv import dotenv_values
from getpass import getpass

__version__ = "0.3.3"


def login(session, username, password):
    payload = {
        "Selected_Action": "login",
        "Menu_Item_ID": 49792,
        "Form_ID": 7323,
        "Pass": 1,
        "Current_URL": "https://www.troopwebhost.org/formCustom.aspx",
        "User_Login": username,
        "User_Password": password,
    }
    p = session.post("https://www.troopwebhost.org/formCustom.aspx", data=payload)
    return "Log Off" in p.text


def get_logged_in_session(username, password, troop_id):
    with requests.Session() as session:
        session.cookies.set("Application_ID", troop_id)
        if login(session, username, password):
            return session
        return None


def get_report(session, report_number):
    return session.get(
        f"https://www.troopwebhost.org/FormReport.aspx?Menu_Item_ID={report_number}&Stack=1&ReportFormat=XLS"
    )


def main(env=None, config_file=None, username=None, troop_id=None):
    if config_file:
        CONFIG = toml.load(config_file)
    else:
        CONFIG = toml.load(Path(__file__).parent / "config.toml")
    if env:
        CONFIG |= dotenv_values(env)
    else:
        CONFIG |= dotenv_values(".env")
    username = username or CONFIG["username"] or input("Username on troopwebhost: ")

    password = CONFIG["password"] or getpass(
        f"Enter Troopwebhost password for {username}: "
    )

    troop_id = CONFIG["troop_id"] or input("Troop ID on troopwebhost: ")

    if session := get_logged_in_session(username, password, troop_id):
        for name, report_number in CONFIG["REPORTS"].items():
            with open(Path(f"{CONFIG['troop_prefix']}{name}.csv"), "wb") as f:
                f.write(get_report(session, report_number).content)


if __name__ == "__main__":
    main()
