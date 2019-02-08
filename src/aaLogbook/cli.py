"""
TODO output options for all save files
TODO more than one save format at a time
TODO save/load output proflies to a file.
TODO for csv, allow list of output fields to be loaded from file
TODO save a list of possible output fields to a file
TODO allow different duration formats in csv
"""

import logging
import click
from pathlib import Path
from aaLogbook.logbookTranslation import save_logbookCsv, save_logbookJson, buildLogbook
from aaLogbook.xmlTranslation import parseXML, saveRawCsv, saveRawFlatJson, saveRawJson
from aaLogbook.models.xmlElementModel import LogbookElement


#### setting up logger ####
logger = logging.getLogger(__name__)

#### Log Level ####
# NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
log_level = logging.DEBUG
# logLevel = logging.INFO
logger.setLevel(log_level)

#### Log Handler ####
log_formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="More verbose output, can be used more than once for even more output",
)
@click.pass_context
def main(ctx, verbose):
    """this is the main help
    """
    pass


# def loadXML(fileIn: Path, parseContext: dict) -> LogbookElement:
#     data = parseXML(fileIn, parseContext)
#     return data


@main.command()  # type: ignore
@click.argument(
    "filein", type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.argument("fileout", type=click.Path(resolve_path=True, writable=True))
@click.option(
    "-e",
    "--export-format",
    type=click.Choice(
        ["rawflatjson", "rawcsv", "rawjson", "translatedcsv", "translatedjson"]
    ),
    default="translatedcsv",
)
@click.pass_context
def export(ctx, filein, fileout, export_format):
    """Export in one of the selected formats. The default format is translatedcsv.

    To export in the default format (translated.csv):

    aaLogbookExport export <path to input file> <path to output file>

    To export in one of the other supported formats:

    aaLogbookExport export -e rawcsv <path to input file> <path to output file>

    For more verbose output:

    aaLogbookExport -v export -e rawcsv <path to input file> <path to output file>

    The raw formats strip all the useful information out of the xml input file,
    but do not transfor the data, or do any consistency checks.

    The transformed formats provide extra fields derived from the raw information,
    and do checks to verify the input data.

    \b
    rawjson             All of the useful information stripped from
                        the XML file, saved in the .json file format.
    rawflatjson         As rawjson above, but flattened down to one
                        entry per flight.
    rawcsv              As rawjson above, but saved in the .csv file
                        format. The first row is columns headers.
    translatedjson      As rawjson above, but with more fields derived
                        from the raw data. IATA, ICAO, airport time zone,
                        dates and times in UTC, etc.
    translatedcsv       As translatedjson above, but flattened to one
                        flight per line. Even more data fields, to 
                        include local times, durations in HH:MM:SS format
                        and duty period number.

    """
    exportDispatch = {
        "rawflatjson": saveFlattenedRawLogbookAsJson,
        "rawcsv": saveFlattenedRawLogbookAsCsv,
        "rawjson": saveRawLogbookAsJson,
        "translatedcsv": saveTranslatedLogbookAsCsv,
        "translatedjson": saveTranslatedLogbookAsJson,
    }
    fileInPath = Path(filein)
    fileOutPath = Path(fileout)
    exportDispatch[export_format](ctx, fileInPath, fileOutPath)


def saveRawLogbookAsJson(ctx: dict, fileIn: Path, fileOut: Path):
    parseContext: dict = {}
    saveRawJson(fileIn, fileOut, parseContext)


def saveFlattenedRawLogbookAsJson(ctx: dict, fileIn: Path, fileOut: Path):
    parseContext: dict = {}
    saveRawFlatJson(fileIn, fileOut, parseContext)


def saveFlattenedRawLogbookAsCsv(ctx: dict, fileIn: Path, fileOut: Path):
    parseContext: dict = {}
    saveRawCsv(fileIn, fileOut, parseContext)


def saveTranslatedLogbookAsJson(ctx: dict, fileIn: Path, fileOut: Path):
    parseContext: dict = {}
    data = parseXML(fileIn, parseContext)
    data = buildLogbook(data)
    save_logbookJson(data, fileOut, parseContext)


def saveTranslatedLogbookAsCsv(ctx: dict, fileIn: Path, fileOut: Path):
    parseContext: dict = {}
    data = parseXML(fileIn, parseContext)
    data = buildLogbook(data)
    save_logbookCsv(data, fileOut, parseContext)


# if __name__ == '__main__':
#     main()
