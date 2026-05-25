import typing


def config_pars() -> dict[str, str]:
    with open("config.txt", "r") as file:
        content = file.readline()
        print(content)

config_pars()