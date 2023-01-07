import argparse
from utils import *

def main(input_file, output_file):
    output = open(output_file, 'w')

    with open(input_file) as input:
        for line in input:
            [filename1, filename2] = line.strip().split(' ', 1)
            if (not (file_exists(filename1) and file_exists(filename2))):
                output.write("Invalid file paths: " + "'" + filename1 + "'" + "'" + filename2 + "'\n")
                continue
            
            output.write("Both files exist: " + "'" + filename1 + "'" + "'" + filename2 + "'\n")
    
    output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument parser')
    parser.add_argument('input_file', default="input.txt", help="Specify input filename")
    parser.add_argument('output_file', default="scores.txt", help="Specify output filename")
    args = parser.parse_args()

    check_file_exists(args.input_file)
    main(args.input_file, args.output_file)
