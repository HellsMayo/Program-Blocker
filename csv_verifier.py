import csv
import os

from global_constants import default_csv
from checker import csv_iterator


def main():
    with open("temp.csv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        count = 1
        for row in csv_iterator(default_csv):
            row[0].replace(' ', '_')
            row[2] = reformat_time(row[2], 'Start', count, row[0])
            row[3] = reformat_time(row[3], 'End', count, row[0])
            csv_writer.writerow(row)
            count += 1
    os.remove(default_csv)
    os.rename("temp.csv", default_csv)


def reformat_time(time, s_or_e, num, program):
    if len(time) == 5:
        if time[2] == ':':
            if 0 <= int(time[:2]) <= 23:
                if 0 <= int(time[3:]) <= 59:
                    return time
    print("%s time \"%s\" for program \"%s\" in row \"%s\" is incorrectly formatted." % (s_or_e, time, num, program))
    return reformat_time(input("Input properly formatted time:"), s_or_e, num, program)


if __name__ == '__main__':
    main()
