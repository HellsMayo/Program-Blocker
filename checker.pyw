import psutil
import csv
import datetime
import winreg
import subprocess

from global_constants import default_hkey, default_key, default_csv, visible_caller_path


def main():
    # if the program visible_caller.py is currently running as a program, stop this process
    if check_python_process('visible_caller'):
        raise SystemExit

    # blocking_str in the format: key_name|key_value|...|
    blocking_str = ""
    # unblocking_str in the format: key_name|...|
    unblocking_str = ""

    # iterate over each row in default_csv
    for row in csv_iterator(default_csv):
        # if current time is between blocking start time, row[2], and blocking end time, row[3]
        if time_range(s_hour=int(row[2][:2]), s_min=int(row[2][3:]), e_hour=int(row[3][:2]), e_min=int(row[3][3:])):
            # and if the register key doesn't exist
            if not value_exists(default_hkey, default_key, row[0]):
                # add the key name, row[0], and key value, row[1], to blocking_str
                blocking_str += row[0] + '|'
                blocking_str += row[1] + '|'

        # if current time is outside of blocking start and blocking end and the register does exist
        else:
            # and if the register exists
            if value_exists(default_hkey, default_key, row[0]):
                # add the key name, row[0], to unblocking_str
                unblocking_str += row[0] + '|'

    # if values were added to blocking_str
    if blocking_str:
        if blocking_str[-1] == '|':
            # remove the last character
            blocking_str = blocking_str[:-1]

        # call the command line
        # run visible_caller.py passing it the variables 'block' and the string of key names and key values
        subprocess.call("start /wait python \"%s\" \"%s\" \"%s\"" % (visible_caller_path, 'block', blocking_str), shell=True)

    # if values were added to unblocking_str
    if unblocking_str:
        if unblocking_str[-1] == '|':
            # remove the last character
            unblocking_str = unblocking_str[:-1]

        # call the command line
        # run visible_caller.py passing it the variables 'unblock' and the string of key names
        subprocess.call("start /wait python \"%s\" \"%s\" \"%s\"" % (visible_caller_path, 'unblock', unblocking_str), shell=True)


def check_python_process(process_name):
    for p in psutil.process_iter():
        if p.name() == 'python.exe':
            for cmd in p.cmdline():
                if process_name in cmd:
                    return True


def csv_iterator(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row:
                yield row


def time_range(s_hour, s_min, e_hour, e_min):
    current_time = datetime.datetime.now()
    start_time = current_time.replace(hour=s_hour, minute=s_min)
    end_time = current_time.replace(hour=e_hour, minute=e_min)
    if end_time < start_time:
        return start_time <= current_time or current_time < end_time
    return start_time <= current_time < end_time


def value_exists(hkey, key, value_name):
    with winreg.OpenKey(hkey, key) as key:
        try:
            winreg.QueryValueEx(key, value_name)
            return True
        except FileNotFoundError:
            return False


if __name__ == '__main__':
    main()
