import os
import errno
import json

#import sys
#sys.path.append('..')
from midi_parser.parse_midi import MIDI_Converter

log_tag = "[save_to_file.py]"


def convertSingleFile(filepath, output):
    '''
    Example for how to convert a single file and export it.
    '''

    #if not output.endswith("/"):
    #    output += "/"

    print("\nCreating possible missing directories...")
    checkPath(output)

    MC = MIDI_Converter()
    results = MC.convert(filepath)

    if results is None or len(results) == 0:
        print("No results.")
    elif 'success' in results and results['success'] and 'data' in results:

        with open(output, "w") as outputfile:
            for data in results['data']:
                outputfile.write(json.dumps(data))
                outputfile.write("\n")

        print("\nExported result to " + output)


    # Example: How to load the jsonl file after exporting it.
    '''
    with open(output, "r") as outin:
        data = []
        for line in outin:
            data.append(json.loads(line))
        # print name of the first element
        print(data[0]['name'])
    '''


def convertMultipleFiles(folderpath, output, logger=None):
    '''
    Converts multiple files from MIDI to JSON.
    Returns a list with paths to the converted files or None!
    '''

    if not output.endswith("/"):
        output += "/"

    if not logger is None:
        logger.info("{} Creating possible missing directories...".format(log_tag))
    checkPath(output)

    # convert all the files and get their JSON representation
    MC = MIDI_Converter()
    results = MC.convertAllFiles(inputPath=folderpath)

    # paths to the converted files
    paths = []

    # check if we got a valid result
    if results is None or len(results) == 0:
        if not logger is None:
            logger.info("{} No results.".format(log_tag))
        else:
            print("{} No results.".format(log_tag))

    elif 'success' in results and results['success'] and 'data' in results:

        # each result is one file
        for result in results['data']:
            filenameout = output + result['filename'] + ".jsonl"

            with open(filenameout, "w") as outfile:
                for element in result['data']:
                    outfile.write(json.dumps(element))
                    outfile.write("\n")

            paths.append(filenameout)

        if not logger is None:
            logger.info("{} Exported all results to {}".format(log_tag, output))
        else:
            print("{} Exported all results to {}".format(log_tag, output))

    return paths


def checkPath(path):
    '''
    Creates possible missing directories.
    '''

    print(" >> {}".format(path))
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                print("Failed to create directory!")
                raise
