# calgen
A simple Python script to generate calendar events, e.g. a training plan, in [iCalendar](https://icalendar.org/) format 
from a [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file.

The output is suitable for importing into every calendar apps that supports the iCalendar format.

# Usage
`calgen.py [-h] (-s START_DATE | -e EVENT_DATE) -i INPUT_FILE -o OUTPUT_FILE`

```
optional arguments:
  -h, --help            show this help message and exit
  -s START_DATE, --start START_DATE
                        start date in format "YYYY-MM-DD"
  -e EVENT_DATE, --event EVENT_DATE
                        event date in format "YYYY-MM-DD"
  -i INPUT_FILE, --input INPUT_FILE
                        path to input file
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        path to output file
```

## Start or event date
You must either specify a start date or and event date, but not both, using the corresponding command-line options.

If you specify a start date (`-s/--start YYYY-MM-DD`), then for each entry from the input file, a calendar event is 
generated where the event's date is determined by adding the event's day offset (an integer) to the start date. 

If you specify an event date (`-e/--event YYYY-MM-DD`), then the start date is determined by subtracting the largest day
offset found in the input file from the given date. This is useful if the input is e.g. a training calendar that targets 
an event on a given day. Rather than calculating on which day the first entry needs to be placed so that the plan ends 
on the event date, you can just specify the date of the target event itself. In your input, the entry with the largest 
day offset must then correspond to the target event.

See `input.csv` for an example of how to specify day offsets.  

## Input file
The input file must be a `csv` file using semicolon `;` as the field delimiter. The script tries to sniff other 
properties of the used csv dialect. Blank lines or text after a hash character `#` are treated as commentary and are 
removed before the input is processed.

See `input.csv` for a valid example (in German).

## Output file
The output file contains the generated calendar events in [iCalendar](https://icalendar.org/) format. This format can be
imported into most common calendar applications.

# Why
For years I used to use free online training plans from [Runner's World](https://www.runnersworld.de/trainingsplaene/).
The site could also generate plans with dates relative to a given start or event date. Also, plans could be exported to
a file in [iCalendar](https://icalendar.org/) format.

As of this year, the plans are no longer available free of charge. Instead, you need to buy each plan for EUR 9,90. 
Given that all plans have been in the public domain for years, I created this script and re-created a plan I used from a 
previously exported [iCalendar](https://icalendar.org/) file.
