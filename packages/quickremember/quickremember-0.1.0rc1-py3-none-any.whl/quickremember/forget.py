import sys
from typing import List
from .consts import FULL_SAVE_PATH
import thefuzz.process as fuz_process


def forget(everything: bool|None=False, search_term: str|None=None) -> None:
    """
    Function to remove from file.
    """
    if everything:
        confirmation = input("Erase memories? (y/N): ")
        if confirmation.lower() == "y":
            with open(FULL_SAVE_PATH, "wt", encoding="utf-8") as f:
                pass
        return
    with open(FULL_SAVE_PATH, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    matches = fuz_process.extract(search_term, lines, limit=1)
    print("Found match:", matches[0][0])
    confirmation = input("Erase memory? (y/N): ")
    if not confirmation.lower() == "y":
        return
    
    lines.remove(matches[0][0])
    with open(FULL_SAVE_PATH, "wt", encoding="utf-8") as f:
        for line in lines:
            f.write(line)

def main(args: List[str]) -> None:
    """
    Forget the "memories" closest matching the input.
    """
    if len(args) < 2:
        print("No information passed.")
        return
    # Check for --everything
    if "--everything" in args:
        forget(everything=True)
        return

    # Otherwise just take the keywords
    search_term = " ".join(args[1:])
    forget(search_term=search_term)

def consolemain() -> None:
    return main(sys.argv)

if __name__ == "__main__":
    main(sys.argv)
