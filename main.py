import argparse
from midi_parser.parse_midi import MIDI_Converter as MC
import midi_parser.save_to_file as stf


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # e.g.
    # parser.add_argument("-l", "--logfile", required=False, help="Set the path and name of the log file", default="./output/ma_log.log")

    args = parser.parse_args()

    print("TODO!")


if __name__ == "__main__":
    main()
