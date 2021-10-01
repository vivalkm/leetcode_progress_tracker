import main
import argparse

parser = argparse.ArgumentParser(prog="tracker_cli")

parser.add_argument(
    "-a",
    "--all",
    help = "Show all accepted submissions by date.",
    action = 'store_true',
    default = 0,
)

parser.add_argument(
    "-n",
    "--ndays",
    help = "Show accepted submissions in recent 10 days.",
    action = 'store_true',
    default = 0,
)

args = parser.parse_args()
if args.all:
    main.allSubmission()
elif args.ndays:
    while True:
        try:
            days = int(input("How many days of records to show? "))
            break
        except:
            print("Please input a number.")
            pass
    main.recentNDaySubmission(days)
