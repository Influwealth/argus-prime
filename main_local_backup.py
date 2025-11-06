import argparse

def activate_capsule(capsule_name):
    """Activates a capsule."""
    print(f"Activating capsule '{capsule_name}'...")

def activate_mindmax():
    """Activates the mindmax capsule."""
    print("Activating capsule 'mindmax'...")

def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Capsule management script.")
    subparsers = parser.add_subparsers(dest="command")

    # Activate command
    activate_parser = subparsers.add_parser("activate", help="Activate a capsule.")
    activate_parser.add_argument("capsule_name", help="The name of the capsule to activate.")

    args = parser.parse_args()

    if args.command == "activate" and args.capsule_name == "argus-prime":
        activate_capsule(args.capsule_name)
    elif args.command == "activate" and args.capsule_name == "mindmax":
        activate_mindmax()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()