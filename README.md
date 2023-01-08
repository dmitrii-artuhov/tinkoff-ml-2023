# Tinkoff ML 2023 enrollment project

## Anti - plagiarism

Utility for comparing python codefiles in order to check for plagiate. 

## How to use
1. Clone the project: `git clone https://github.com/dmitrii-artuhov/tinkoff-ml-2023.git`.
2. Install at least `Python 3.9.x` (ver. `3.10.9` was used during development).
3. Run the command:
    ```python
    python compare.py input.txt output.txt
    ```
    where `input.txt` contains pairs of files to be compared, eg.:
    ```txt
    plagiat/1.py plagiat/2.py
    plagiat/2.py plagiat/2.py
    plagiat/1.py plagiat/not-found.py
    ```

    In the output file you will find floating point numbers (the scores in range `[0, 1]`, the bigger the score, the more similar the programms are), eg.:

    ```txt
    0.7687309644670051
    1.0
    Invalid path(s): 'plagiat/not-found.py'
    ```

## How it works
Programm uses [Levenstein distance](https://en.wikipedia.org/wiki/Levenshtein_distance#:~:text=Informally%2C%20the%20Levenshtein%20distance%20between,considered%20this%20distance%20in%201965.) algorithm on the pre-processed python-programm texts. To be exact, the formula look like this: `compare(a, b) = levenstein_distance(a, b) / max(len(a), len(b))`, where `a` and `b` the programm texts and `compare(a, b)` is the function that calculates the final answer. 

Text pre-processing does the following:

1. Removes all `docstrings` in the programm.
2. Renames all variables to the pattern: `var_{i}` (where `i` is the number of the variables that were renamed before variable `var_{i}`) and substitutes them with their pattern-name.
3. Renames all functions, including class methods to the pattern: `func_{i}`, following same rule as described above.
4. Renames all function and method arguments (except `self` keyword) and substitutes them with their pattern-name inside the function/method body.