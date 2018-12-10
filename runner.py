import argparse
import os

import termcolor

import itertools
import threading

from datetime import datetime, timedelta
from aocd import AOC_TZ

import time

from days import days


def parse_args():
    parser = argparse.ArgumentParser(description='Solve Advent of Code Problems')
    parser.add_argument("--days", type=int, nargs="+", help="days to run. Default is to run all")
    parser.add_argument("--timed", action="store_true", help="Time how long it takes to get the answer for each day")
    parser.add_argument("--submit", action="store_true", help="Submit answers with session token")
    parser.add_argument("--session", type=str, help="Advent of Code session token to retrieve input and submit "
                                                    "answers")
    # parser.add_argument("--sequential", action="store_true", help="Run each day one after the other")

    args = parser.parse_args()

    if args.submit and (args.days is None or len(args.days) > 1):
        termcolor.cprint(
            "When submitting answers please specify a single day", color="red")
        exit(-1)

    if args.days is None:
        args.days = list(range(1, 11))

    if max(args.days) > 25 or min(args.days) < 1:
        termcolor.cprint(
            "Days outside of range (1-25)", color="red")
        exit(-1)

    if args.session is not None:
        os.putenv("AOC_SESSION", args.session)

    return args


def spinning_bar(day: int, stop_event: threading.Event):
    for i in itertools.cycle(["|", "/", "-", "\\"]):
        print(f"\rDay {day}: {i}", end="")
        if stop_event.wait(0.25):
            break


def main():
    args = parse_args()

    print("David's Advent of Code solver")

    args.days.sort()

    for day in args.days:
        if day not in days:
            aoc_now = datetime.now(tz=AOC_TZ)
            if aoc_now.month != 12 or aoc_now.day >= day:
                termcolor.cprint(f"Unfortunately I haven't been able to do day {day}", color="red")
                break
            if aoc_now.day < day:
                termcolor.cprint(f"Unfortunately I don't have a time machine to do day {day}", color="red")
                break

        stop_spinning_bar = threading.Event()
        spinning_bar_thread = threading.Thread(target=spinning_bar, name="Spinning Bar", args=(day, stop_spinning_bar))
        spinning_bar_thread.start()

        start = time.perf_counter()

        part1, part2 = days[day](args.submit)

        end = time.perf_counter()
        end_time = datetime(1, 1, 1) + timedelta(seconds=(end - start))

        stop_spinning_bar.set()
        spinning_bar_thread.join()

        print(f"\rDay {day}:")
        if args.timed:
            print(f"\r\tTime: {end_time:%H:%M:%S.%f}")
        print(f"\r\tPart 1: {part1}")
        print(f"\r\tPart 2: {part2}\n")


if __name__ == "__main__":
    main()
