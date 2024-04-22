import sys
from typing import List
import os
from thefuzz import process as fuz_process
from .consts import SAVE_DIR, FULL_SAVE_PATH

def fuzzy_file(search_term: str, f) -> None:
    """
    Using the file handle, fuzzy search for a line with the data.
    """
    lines = f.readlines()

    matches = fuz_process.extract(search_term, lines, limit=5)
    print("Found", len(matches), "closest matching memories.")
    print()

    for match in matches:
        print(match[0].strip())

def recall(everything: bool=False, search_term: str|None=None) -> None:
    """
    Recall some of the saved data and print it to screen.
    """
    os.makedirs(SAVE_DIR, exist_ok=True)
    try:
        with open(FULL_SAVE_PATH, "rt", encoding="utf-8") as f:
            if everything:
                print(f.read().strip())
            else:
                fuzzy_file(search_term, f)
    except FileNotFoundError:
        print("No memories found!")

def remember(what: str) -> None:
    """
    Literally just take what we want to remember and append it to a file.
    That's it.
    """
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(FULL_SAVE_PATH, "at", encoding="utf-8") as f:
        f.write(f"{what}\n")

def main(args: List[str]) -> None:
    """
    Remember something! When you need to remember something, why make some random file you may never see again?
    Instead, just say remember. Remember is not a todo list, it's simply to remember some bit of information
    to recall at a later date.
    Example usage:
        `remember python is cool`
        `remember my api key is asdfjkl;`
        `remember api key?`
        `remember python?`
        `remember --everything`
        `forget --everything`
        `forget python is cool` - forget erases closest match
    """
    if len(args) < 2:
        print("No information passed.")
        return
    # We need to start by determining if we are remembering something or recalling something.

    # Check for --everything flag.
    if "--everything" in args:
        return recall(everything=True)

    # condense all args aside from program arg into one string
    query: str = " ".join(args[1:]).strip()

    # Determine if it's a search query by the existence of a "?" as the last character
    if query[-1] == "?":
        return recall(search_term=query[:-1])

    # It's clearly not a search query of any sort so let's insert something to remember
    return remember(query)

def consolemain() -> None:
    return main(sys.argv)

if __name__ == "__main__":
    main(sys.argv)
