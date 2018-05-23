from parse_midi import MIDI_Converter
import os
import errno
import json


def convertSingleFile(filepath, output):
    '''
    Example for how to convert a single file and export it.
    '''

    if not output.endswith("/"):
        output += "/"

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


def convertMultipleFiles(folderpath, output):
    '''
    Example for how to convert all files of a folder.
    '''

    if not output.endswith("/"):
        output += "/"

    print("\nCreating possible missing directories...")
    checkPath(output)

    MC = MIDI_Converter()
    results = MC.convertFiles(folderpath)

    # check if we got a valid result
    if results is None or len(results) == 0:
        print("No results.")
    elif 'success' in results and results['success'] and 'data' in results:

        # each result is one file
        for result in results['data']:
            filenameout = output + result['filename'] + ".jsonl"

            with open(filenameout, "w") as outfile:
                for element in result['data']:
                    outfile.write(json.dumps(element))
                    outfile.write("\n")

        print("\nExported all results to " + output)


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
