from pathlib import Path
from robot.api import logger
from Variables import config


def browser_path():
    browser_directory = config.BROWSER_DIRECTORY
    logger.info(f'Configurando o Selenium para '
                f'rodar com o chrome {browser_directory}')
    if not Path(browser_directory).is_file():
        raise ValueError(f'O Browser para a versão especificada no '
                         f'projeto não está no local {browser_directory}')
    return browser_directory


def chromedriver_path():
    chromedriver_directory = config.CHROMEDRIVER_DIRECTORY
    logger.info(f'Configurando o Selenium para '
                f'rodar com o driver {chromedriver_directory}')
    if not Path(chromedriver_directory).is_file():
        raise ValueError(f'O chromedriver.exe para a versão especificada no '
                         f'projeto não está no local {chromedriver_directory}')
    return chromedriver_directory
