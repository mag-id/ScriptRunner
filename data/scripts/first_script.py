from sys import argv
from time import sleep


def main():

    print("Start FIRST script.")

    if len(argv) > 2:
        raise ValueError("Script takes only one argument.")
    elif len(argv) < 2:
        raise ValueError("Script argument is not specified.")

    time = int(argv[1])
    print(f"Sleep {time} seconds...")

    sleep(time)
    print("End FIRST script.")


if __name__ == "__main__":
    main()
