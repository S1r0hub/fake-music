from music21 import stream, note, instrument


class Postprocessor():

    def __init__(self, logger=None):
        self.logger = logger


    def export_midi(self, notes, filepath):
        '''
        output_notes = the generated notes
        filepath = the path and the filename without filextension!
        '''

        output_notes = []
        offset = 0


        # bring notes to midi21 format
        for pattern in notes:
            # TODO: check if pattern is a chord
            # TODO: separate duration and use it instead of offset

            try:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                output_notes.append(new_note)
            except Exception as e:
                self.logger.error('Failed to add a note pattern "{}"! ({})'.format(pattern, str(e)))


        if len(output_notes) == 0:
            self.logger.warning("Nothing to export!")
            return False


        # write notes to file
        try:
            midi_stream = stream.Stream(output_notes)
            midi_stream.write('midi', fp=filepath + ".mid")
            midi_stream.write('mp3', fp=filepath + ".mp3")
            #midi_stream.show('midi') # to hear the stream
        except Exception as e:
            self.logger.error("Failed to export to midi! ({})".format(str(e)))
            return False

        return True
