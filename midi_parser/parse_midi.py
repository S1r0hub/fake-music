import music21
import json
import glob
import os
from collections import OrderedDict


class MIDI_Converter():

    def __init__(self):
        pass


    def printError(self, errormsg):
        return {
            'success': False,
            'reason': errormsg
        }


    def convert(self, path):
        '''
        Converts a MIDI file to our needed table format.
        Returns a set with the following keys:
        - success
        - filename
        - data
        '''

        # check if files exist before continuing
        if not os.path.isfile(path):
            return self.printError("File does not exist!")

        # check file ending (TODO:  or path.endswith(".midi"))
        if not (path.endswith(".mid")):
            return self.printError("Wrong file format!")

  
        midi = music21.converter.parse(path)
        instruments = music21.instrument.partitionByInstrument(midi)
        parse_notes = None
        output = []

        if instruments:
            parse_notes = instruments.parts[0].recurse()
        else:
            parse_notes = midi.flat.notes

        for e in parse_notes:
            if isinstance(e, music21.note.Note):
                output.append(OrderedDict([
                    ('type', 'note'),
                    ('name', str(e.name)),
                    ('octave', int(e.octave)),
                    ('pitch', str(e.pitch)), # combination of the both before
                    ('offset', float(e.offset)),
                    ('duration', self.getDuration(e.duration.quarterLength))
                ]))
            elif isinstance(e, music21.chord.Chord):
                #chord_notes = [int(n) for n in e.normalOrder]
                chord_notes = [str(p) for p in e.pitches]
                output.append(OrderedDict([
                    ('type', 'chord'),
                    ('name', str(e.commonName)),
                    ('offset', float(e.offset)),
                    ('duration', self.getDuration(e.duration.quarterLength)),
                    ('pitch', chord_notes)
                ]))

        # get just the filename
        pathsplit = path.rsplit("/",1)
        filename = pathsplit[-1:][0]

        return {
            'success': True,
            'filename': filename,
            'data': output
        }


    def getDuration(self, durationIn):
        ''' Get the duration as a float value of a string.
            Returns 1.0 if converting fails! '''

        duration = 1.0

        try:
            durstr = str(durationIn)
            # check for fraction
            dursplit = durstr.split("/")
            if len(dursplit) > 1:
                duration = round(float(dursplit[0]) / float(dursplit[1]), 2)
            else:
                duration = float(durstr)
        except Exception as n:
            print("Failed to convert duration: " + durstr)
            print(n)

        return duration


    def convertFiles(self, inputPath, outputPath=None, logger=None):
        '''
        Converts all the MIDI files of the folder.
        - inputPath = path where the MIDI files are located
        - outputPath = Location where to put the files in.

        ## WITHOUT outputPath:
        Returns the following structure if outputPath is NOT given:
        {
            "success": <bool>,
            "data": [
                {
                    "filename": <str>,
                    "filepath": <str>,
                    "data":
                    [
                        {
                            "type": <str>,
                            "name": <str>,
                            ...
                        },
                        ...
                    ]
                },
                ...
            ]
        }

        ## WITH outputPath given:
        Returns a set if the outputPath IS given but with data
        being a list that contains paths to each converted file!
        {
            "success": <bool>,
            "data": [
                filepath.json,
                filepath2.json,
                ...
            ]
        }
        '''

        if not inputPath.endswith("/"):
            inputPath += "/"


        # validate output folder if given
        if not outputPath is None:
            if not outputPath.endswith("/"):
                outputPath += "/"
            
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)


        output = []
        tag = "[parse_midi.py] "

        for file in glob.glob(inputPath + "*.mid"):
            result = self.convert(file)
            if result['success']:

                # export to file if output parameter given
                if not outputPath is None:
            
                    filepath = outputPath + result['filename'] + ".jsonl"

                    try:
                        # write converted data to file
                        with open(filenameout, "w") as outfile:
                            for element in result['data']:
                                outfile.write(json.dumps(element))
                                outfile.write("\n")

                        msg = tag + "MIDI file converted to JSON: {}".format(filepath)
                        if not logger is None: logger.info(msg)
                        else: print(msg)

                    except Exception as e:
                        msg = tag + "Failed to convert MIDI! ({})".format(str(e))
                        if not logger is None: logger.error(msg)
                        else: print(msg)

                else:

                    output.append(OrderedDict([
                        ('filename', result['filename']),
                        ('filepath', file),
                        ('data', result['data'])
                    ]))


        if len(output) == 0:
            msg = tag + "No files parsed. (No MIDI files given)"
            if not logger is None: logger.info(msg)
            else: print(msg)

        elif not outputPath is None:
            msg = tag + "Files exported: {}".format(len(output))
            if not logger is None: logger.info(msg)
            else: print(msg)

        return {
            'success': True,
            'data': output
        }
