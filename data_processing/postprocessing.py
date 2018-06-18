from music21 import stream, note, instrument, duration


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
            if ('_' in pattern or pattern.isdigit() ):
                try:
                    note_dura = pattern.split('_')
                    notes =  note_dura[0]
                    note_duration = float(note_dura[1])
                    new_note = note.Note(notes, quarterLength=note_duration)
                    new_note.offset = offset + float(note_dura[2])
                    new_note.duration = duration.Duration()
                    new_note.storedInstrument = instrument.Piano()
                    output_notes.append(new_note)
                    offset += float(note_dura[2])
                except Exception as e:
                    self.logger.error('Failed to add a note pattern "{}"! ({})'.format(pattern, str(e)))
            else:
                try:
                    new_note = note.Note(pattern)
                    new_note.offset = offset
                    new_note.storedInstrument = instrument.Piano()
                    output_notes.append(new_note)
                    offset += 0.5
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
