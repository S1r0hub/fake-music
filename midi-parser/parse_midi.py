import music21
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
                    ('duration', self.getDuration(e.duration.quarterLength))
                ]))
            elif isinstance(e, music21.chord.Chord):
                chord_notes = [int(n) for n in e.normalOrder]
                output.append(OrderedDict([
                    ('type', 'chord'),
                    ('name', str(e.commonName)),
                    ('duration', self.getDuration(e.duration.quarterLength)),
                    ('notes', chord_notes)
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


    def convertFiles(self, folder_path):
        '''
        Converts all the MIDI files of the folder.

        Returns the following structure:
        [
            {
                'filename': <str>,
                'filepath': <str>,
                'data':
                [
                    {
                        'type': <str>,
                        'name': <str>,
                        ...
                    },
                    ...
                ]
            },
            ...
        ]
        '''

        if not folder_path.endswith("/"):
            folder_path += "/"

        output = []

        for file in glob.glob(folder_path + "*.mid"):
            result = self.convert(file)
            if result['success']:
                output.append(OrderedDict([
                    ('filename', result['filename']),
                    ('filepath', file),
                    ('data', result['data'])
                ]))

        if len(output) == 0:
            print("No MIDI files found.")

        return {
            'success': True,
            'data': output
        }
