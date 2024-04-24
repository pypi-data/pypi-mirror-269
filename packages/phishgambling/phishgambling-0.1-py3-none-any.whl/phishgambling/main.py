import time
import sys
import os


class colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def victimScan():
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(2)
    print("\n{}Victim Scanned the QR!{}".format(colors.GREEN, colors.END))
    time.sleep(2)
    print("\nCollecting Basic Information.....\n ")


def fake_loading():
    print("Loading:", end=" ")
    for i in range(101):
        sys.stdout.write("\r")
        sys.stdout.write(
            "{}[{}%0s] {}%[{}s]".format(
                colors.YELLOW, colors.RED, "=" * i, i, colors.END
            )
        )
        sys.stdout.flush()
        time.sleep(0.01)

    print("{}\nLoading complete!{}".format(colors.GREEN, colors.END))
    time.sleep(1.5)


def fake_credentials():
    os.system("cls" if os.name == "nt" else "clear")
    width = 69  # Width of the box, subtracting one '='
    line = "=" * width
    print("\n" + line)
    time.sleep(0.5)
    print("{:<41}".format("Address: Punta OC, Leyte, Philippines"))
    time.sleep(0.5)
    print("{:<41}".format("Device: LG MODEL"))
    time.sleep(0.5)
    print("{:<41}".format("Age: 18"))
    time.sleep(0.5)
    print("{:<41}".format("Email: lopez"))
    time.sleep(0.5)
    print("{:<41}".format("Phone: +09090920901"))
    time.sleep(0.5)
    print("{:<41}".format("Occupation: Student"))
    time.sleep(0.5)
    print("{:<41}".format("Interests: Gaming, Programming"))
    time.sleep(0.5)
    print(line)


def main():
    victimScan()
    fake_loading()
    fake_credentials()


if __name__ == "__main__":
    main()
