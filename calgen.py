#!/bin/python
import argparse
import csv
from datetime import datetime, timedelta
from uuid import uuid4

from icalendar import Calendar, Event

from util import decomment, valid_date_type, valid_existing_file_path, valid_writable_file_path


def main():
    """Main entry point.
    :return:
    """

    # Command line option parser.
    parser = argparse.ArgumentParser(description=None)

    # A group of options for either specifying the start date or the event date (=last entry in input file). The user
    # needs to specify exactly one of the options, but they're mutually exclusive.
    date_group = parser.add_mutually_exclusive_group(required=True)

    # Option to specify start date.
    date_group.add_argument('-s', '--start',
                            dest='start_date',
                            type=valid_date_type,
                            default=None,
                            help='start date in format "YYYY-MM-DD"')

    # Option to specify event date.
    date_group.add_argument('-e', '--event',
                            dest='event_date',
                            type=valid_date_type,
                            default=None,
                            help='event date in format "YYYY-MM-DD"')

    # Required option to specify input file.
    parser.add_argument('-i', '--input',
                        dest='input_file',
                        type=valid_existing_file_path,
                        default=None,
                        required=True,
                        help='path to input file')

    # Required option to specify output file.
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        type=valid_writable_file_path,
                        default=None,
                        required=True,
                        help='path to output file')

    # Parse command line options.
    args = parser.parse_args()

    # The list of entries to read from the input file.
    entries = []

    # Open input file and parse contents.
    with open(args.input_file) as input_file:
        # Convert input file to list of strings, removing blank lines and comments after hash.
        input_list = decomment(input_file)

        # The sample to sniff the CSV dialect from.
        sample = ""

        # Try to build a sufficiently large sample from input.
        for line in input_list:
            if len(sample) >= 1024:
                break
            else:
                sample = sample.join(line)

        # Check sample size.
        if len(sample) <= 0:
            print("Unable to determine non-empty sample from input file to deduce CSV dialect.")
            # Cannot continue since we couldn't get any sample. The (decommented) input is probably empty.
            exit(1)

        # Try to deduce CSV dialect.
        dialect = csv.Sniffer().sniff(sample, delimiters=[";"])

        # CHeck if we could determine the CSV dialect.
        if dialect is None:
            print("Unable to determine CSV dialect from input file sample. Using default dialect Excel.")
            # Default to Excel dialect.
            dialect = csv.excel

        # Get new CSV reader using dialect.
        reader = csv.reader(input_list, dialect)

        # Loop over all rows in file.
        for row in reader:
            if len(row) == 3:
                # Row seems to have correct length.
                entries.append(row)
            else:
                # Unexpected length. Log the error and exit.
                print("Could not parse row '{0}' from input file.".format(row))
                exit(1)

    # The entries in the input file will typically be sorted by the day offset relative to the start date anyway, but
    # let's make sure.
    entries.sort(key=lambda e0: int(e0[0]))

    # Determine start date.
    if args.start_date is None:
        # Calculate start date from given event date and the day offset of the last entry. The latter, by assumption,
        # represents the day of the event.
        s = args.event_date + timedelta(days=-int(entries[-1][0]))
    else:
        # Use event date from command line option.
        s = args.start_date

    # Extract the date part. We don't care about the time of the day.
    s = s.date()

    # The current time. Only used to specify the creation time of the calendar events.
    now = datetime.now()

    # Create new calendar.
    c = Calendar()

    # Add essential components.
    c.add('prodid', '-//Jens Keiner//calgen//1.0')
    c.add('version', '2.0')
    c.add('calscale', 'GREGORIAN')

    # Loop over all entries and add a calendar event for each.
    for entry in entries:
        # Determine event date by adding entry's day offset to start date.
        t = s + timedelta(days=int(entry[0]))

        # Determine summary and description.
        summary = entry[1]
        description = "{0}{1}".format(summary, entry[2])

        # Create new calendar event.
        e = Event()
        e.add('transp', 'TRANSPARENT')
        e.add('status', 'CONFIRMED')
        e.add('dtstart', t)
        e.add('dtend', t)
        e.add('dtstamp', now)
        e.add('summary', summary)
        e.add('description', description)
        e.add('uid', uuid4())  # Required as per RFC 5545.

        # Add event to calendar.
        c.add_component(e)

    # Write calendar to output file.
    with open(args.output_file, 'wb') as output_file:
        output_file.write(c.to_ical())


if __name__ == "__main__":
    main()
