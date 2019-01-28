
import logging
import click


#### setting up logger ####
logger = logging.getLogger(__name__)

#### Log Level ####
# NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
log_level = logging.DEBUG
# logLevel = logging.INFO
logger.setLevel(log_level)

#### Log Handler ####
log_formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s", datefmt='%d-%b-%y %H:%M:%S')
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


@click.group()
def main():
    print('cmd Main!')

def loadXML():
    pass

@main.command()# type: ignore
@click.argument('xmlfile',type=click.Path(exists=True,dir_okay=False,resolve_path=True))
@click.argument('outputfile',type=click.Path(resolve_path=True,writable=True))
def export(xmlfile,outputfile):
    print(xmlfile,type(xmlfile))
    print(outputfile,type(outputfile))

def saveRawLogbookAsJson():
    pass

def saveFlattenedRawLogbookAsJson():
    pass

def saveFlattenedRawLogbookAsCsv():
    pass

def saveTranslatedLogbookAsJson():
    pass

def saveTranslatedLogbookAsCsv():
    pass




if __name__ == '__main__':
    main()