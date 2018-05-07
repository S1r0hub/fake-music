import music21
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

        # check file ending
        if not (path.endswith(".mid") or path.endswith(".midi")):
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
                    ('duration', str(e.duration.quarterLength))
                ]))
            elif isinstance(e, music21.chord.Chord):
                chord_notes = [int(n) for n in e.normalOrder]
                output.append(OrderedDict([
                    ('type', 'chord'),
                    ('name', str(e.commonName)),
                    ('duration', str(e.duration.quarterLength)),
                    ('notes', chord_notes)
                ]))

        return {
            'success': True,
            'data': output
        }


    def extractData(self, folder_path):
        '''
        Converts all the MIDI files of the folder.
        '''

        pass
