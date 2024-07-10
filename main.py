#!/usr/bin/python3

import argparse
from algorithms import algorithms

def main():
    parser = argparse.ArgumentParser(description="A program to encode files using different algorithms")
    algorithm_options = [ "huffman" ]
    parser.add_argument("-a", "--algorithm",
                        help="Specifies the algorithm to use",
                        required=True, 
                        metavar='algorithm', 
                        choices=algorithm_options
                        )
    parser.add_argument("-d", "--decode", action="store_true")
    parser.add_argument("input")
    parser.add_argument("output", nargs="?")

    args = parser.parse_args()

    if not args.decode:
        if (args.output):
            output_file = args.output
        else:
            parts = args.input.split(".")
            if len(parts) > 1:
                parts.pop(-1)
            output_file = ".".join(parts) + algorithms[args.algorithm].extension

        encoder = algorithms[args.algorithm].encoder

        encode(args.input, output_file, encoder)

    else:
        print("TODO: Add decoding")

    

def encode(input_file, output_file, encoder):
    with open(input_file, "r") as f_in:
        input = f_in.read()

    output = encoder.encode(input)

    with open(output_file, "wb") as f_out:
        f_out.write(output)


if __name__ == "__main__":
    main()
