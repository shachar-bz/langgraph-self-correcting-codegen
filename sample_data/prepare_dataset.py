"""
prepare_dataset.py

Run this script ONCE before starting Assignment #2 to verify that your working
directory contains all the files you need to develop and test your LangGraph
application against the sample query.

Usage:
    python prepare_dataset.py

Expected output:
    All 6 required files found. You are ready to start working on hw2.py.
"""

import os
import sys

REQUIRED_FILES = [
    "customers.csv",
    "products.csv",
    "orders.csv",
    "query_input.txt",
    "top-spender.txt",
    "top_spender_validate.py",
]


def main():
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    if missing:
        print("ERROR: The following required files are missing from the current directory:")
        for f in missing:
            print(f"  - {f}")
        print()
        print("Make sure you downloaded ALL files from the gist and that you are running")
        print("this script from the same directory where they live.")
        sys.exit(1)

    print("All 6 required files found. You are ready to start working on hw2.py.")
    print()
    print("Next steps:")
    print("  1. Implement your LangGraph application in hw2.py")
    print("  2. Run it with:  python hw2.py")
    print("  3. Verify it produces: top-spender.py, top-spender_answer.txt,")
    print("     top-spender_errors.txt, top-spender_reflect.txt")


if __name__ == "__main__":
    main()
