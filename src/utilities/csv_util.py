# -*- coding: utf-8 -*-
'''Utilities for handling csv files

Todo:
    * Write some tests


Created on Nov 27, 2017

@author: croaker
'''
from pathlib import Path
from collections import namedtuple
from typing import List, Iterable, NamedTuple, Sequence, Dict,Optional
import csv
import logging
from sys import stdout


#### setting up logger ####
logger = logging.getLogger(__name__)

#### Log Level ####
# NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
# log_level = logging.DEBUG
# log_level = logging.INFO
log_level = logging.NOTSET
logger.setLevel(log_level)

#### Log Handler ####
log_formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s", datefmt='%d-%b-%y %H:%M:%S')
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


def writeNamedTuplesToCsv(outPath: Path, data: Sequence[NamedTuple], useColumnHeaders=True, customColumnHeaders: Sequence[str] = None)->bool:
    """Write a namedtuple out to a file in csv format.

    This function will write out a `namedtuple` to a file in CSV format.
    Column headers are taken from the `_fields` attribute of the `namedtuple`
    unless a list of column headers is provided.

    Args:
        outPath: Path to the output file
        ntList: List of `namedtuple`s
        useColumnHeaders: Output column headers on first line.
        customColumnHeaders: List of custom column headers to use instead of `_fields`.
            Providing a list of column headers assumes useColumnHeaders=True

    Returns:
        The return value. True for success, False otherwise.

    Raises:

    """
    if useColumnHeaders or customColumnHeaders:
        if customColumnHeaders:
            # TODO add check for correct number of customColumnHeaders?
            writeListToCsv(outPath, data, customColumnHeaders)
        else:
            writeListToCsv(outPath, data, data[0]._fields)
    else:
        writeListToCsv(outPath, data)
    return True
    # try:
    #     with open(outPath, 'w', newline='', encoding='utf-8') as csvFile:
    #         csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
    #         if useColumnHeaders or customColumnHeaders:
    #             if customColumnHeaders:
    #                 # TODO add check for correct number of customColumnHeaders?
    #                 csvWriter.writerow(customColumnHeaders)
    #             else:
    #                 csvWriter.writerow(ntList[0]._fields)
    #         for row in ntList:
    #             csvWriter.writerow(row)
    # except Exception as e:
    #     logger.exception(f"Error writing csv file to {outPath}")
    #     raise e


def writeListToCsv(outPath: Path, data: Sequence[Sequence], customColumnHeaders: Sequence[str] = None)->bool:
    """Write a list of iterables out to a file in csv format.

    This function will write out a list of iterables to a file in CSV format.
    Column headers may be provided as a list in customColumnHeaders.


    Args:
        outPath: Path to the output file
        dataList: List of `namedtuple`s
        customColumnHeaders: List of custom column headers to use.

    Returns:
        The return value. True for success, False otherwise.

    Raises:

    """
    try:
        with open(outPath, 'w', newline='', encoding='utf-8') as csvFile:
            csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
            if customColumnHeaders:
                csvWriter.writerow(customColumnHeaders)
            for row in data:
                csvWriter.writerow(row)
        return True
    except Exception as e:
        logger.exception(f"Error writing csv file to {outPath}")
        raise e


def writeDictToCsv(outPath: Path, data: Sequence[Dict[str, str]], keyList: Optional[Sequence[str]] = None, useColumnHeaders=True)->bool:
    if len(data) == 0:
        raise ValueError("data is empty. No file written to {outPath} ")
    try:
        with open(outPath, 'w', newline='', encoding='utf-8') as csvFile:
            if keyList:
                csvWriter = csv.DictWriter(csvFile, keyList, quoting=csv.QUOTE_ALL)
            else:
                csvWriter = csv.DictWriter(csvFile, [y for y in data[0].keys()], quoting=csv.QUOTE_ALL)
            if useColumnHeaders:
                csvWriter.writeheader()
            for row in data:
                csvWriter.writerow(row)
        return True
    except Exception as e:
        logger.exception(f"Error writing csv file to {outPath}")
        raise e


def readCsv(inPath: Path, rowFactory=None)->list:
    # TODO rewrite as generator
    with open(inPath, newline='') as csvFile:
        reader = csv.reader(csvFile)
        data: list = []
        for row in reader:
            if rowFactory:
                data.append(rowFactory(*row))
            else:
                data.append(row)
        return data
