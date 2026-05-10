import sys

from cmds.startday import start_day

def main():
    if len(sys.argv) < 2:
        print("Usage: assistant.exe <command>")
        return

    command = sys.argv[1].lower()

    commands = {
        "startday": start_day
    }

    if command in commands:
        commands[command]()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()