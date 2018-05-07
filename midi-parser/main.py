# Example for using the parse_midi.py library usage.


from parse_midi import MIDI_Converter
import json


def main():
    filepath = "./midi/country/sweet-home-alabama.mid"
    output = "out.jsonl"

    MC = MIDI_Converter()
    results = MC.convert(filepath)

    if results is None or len(results) == 0:
        print("No results.")
    elif 'success' in results and results['success'] and 'data' in results:
        with open(output, "w") as outputfile:
            for data in results['data']:
                outputfile.write(json.dumps(data))
                outputfile.write("\n")
        print("Exported results to " + output)


    # Example: How to load the jsonl file after exporting it.
    '''
    with open(output, "r") as outin:
        data = []
        for line in outin:
            data.append(json.loads(line))
        # print name of the first element
        print(data[0]['name'])
    '''


if __name__ == '__main__':
    main()
