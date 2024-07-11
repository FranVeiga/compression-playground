# Compression Playground

This is a project which showcases different compression algorithms. It's goal
is to provide insight on how this algorithms work on a fundamental level.
Currently, the following algorithms are implemented:

- Huffman encoding (WIP)

## Usage

In the project's root directory run the following:

To compress a file:
```
$ ./main.py -a <ALGORITHM> <INPUT_FILE> [<OUTPUT_FILE>]
```

To decode a file:
```
$ ./main.py -d -a <ALGORITHM> <INPUT_FILE> [<OUTPUT_FILE>]
```

To see available algorithms, use `./main.py --list-algorithms`

## Why Python?

Python definitely isn't the best tool for this job, but I think its readability
and ease of use allow for the code to be really didactic. I also just wanted to
make a project in Python!
