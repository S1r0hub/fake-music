# Example for using the parse_midi.py library usage.
import save_to_file


def main():
    output_folder = "./output/"

    print("1. Converting a single file:")
    save_to_file.convertSingleFile("./midi/country/sweet-home-alabama.mid", output_folder + "out.jsonl")

    print("\n\n2. Converting all files of a folder:")
    save_to_file.convertMultipleFiles("./midi/country", output_folder + "all_files/")


if __name__ == '__main__':
    main()
