import argparse
from utils import *

def main(input_file, output_file):
    output = open(output_file, 'w')

    with open(input_file) as input:
        for line in input:
            [filename1, filename2] = line.strip().split(' ', 1)

            is_valid_filename1 = file_exists(filename1)
            is_valid_filename2 = file_exists(filename2)

            if (not (is_valid_filename1 and is_valid_filename2)):
                message = "Invalid path(s): "
                if (not is_valid_filename1):
                    message += f"'{filename1}'"
                if (not is_valid_filename2):
                    message += f", '{filename2}'"
                message += "\n"
                output.write(message)
                continue
                
            output.write(f"Both files exist: '{filename1}', '{filename2}'\n")
    
    output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument parser')
    parser.add_argument('input_file', default="input.txt", help="Specify input filename")
    parser.add_argument('output_file', default="scores.txt", help="Specify output filename")
    args = parser.parse_args()

    check_file_exists(args.input_file)
    main(args.input_file, args.output_file)
