from music21 import stream, note, chord, instrument, duration


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
            if '_' in pattern:
                try:
                    sample = pattern.split('_')

                    if len(sample) < 3:
                        raise Exception('Sample is missing information! (Too short)')

                    # get the information
                    data = {}
                    data['pitch'] =  sample[0]
                    data['duration'] = float(sample[1])
                    data['offset'] = float(sample[2])
                    
                    new_item = None

                    # check if sample is a chord or a note
                    if '/' in data['pitch']:
                        data['pitch'] = data['pitch'].split("/")
                        new_item = self.toChord(data, offset)
                    else:
                        new_item = self.toNote(data, offset)

                    if not new_item is None:
                        # settings that apply for both, notes and chords
                        new_item.storedInstrument = instrument.Piano()

                        # add to output and increase offset
                        output_notes.append(new_item)
                        offset += float(data['offset'])

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


    def toNote(self, data, offset_previous):
        new_note = note.Note(data['pitch'], quarterLength=data['duration'])
        new_note.offset = offset_previous + float(data['offset'])
        #new_note.duration = duration.Duration()
        return new_note

    def toChord(self, data, offset_previous):
        new_chord = chord.Chord(data['pitch'], quarterLength=data['duration'])
        new_chord.offset = offset_previous + float(data['offset'])
        return new_chord
