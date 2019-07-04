import sys
import winreg
import subprocess

from global_constants import default_hkey, default_key


def main():
    # print all passed arguments
    #for string in sys.argv:
    #    print(string)

    if sys.argv[1] == 'unblock':
        unblocking_list = sys.argv[2].split('|')
        for value in unblocking_list:
            unblock_program(value)
        input("All blocks successfully removed. Press enter to close.")

    elif sys.argv[1] == 'block':
        blocking_list = sys.argv[2].split('|')
        assert(len(blocking_list) % 2 == 0)
        for i in range(0, len(blocking_list), 2):
            block_and_kill_program(blocking_list[i], blocking_list[i+1])
        input("All blocks successfully created. Press enter to close.")

    else:
        print("invalid method argument")
        input("Press enter to close.")


def unblock_program(key_name):
    input("Block end time meet for %s. Press enter to remove block." % key_name)
    delete_registry(default_hkey, default_key, key_name)
    print()


def block_and_kill_program(key_name, key_value):
    input("Block start time meet for %s. Press enter to kill program and create block." % key_name)
    close_program(key_value)
    create_registry(default_hkey, default_key, key_name, key_value)
    print()


def create_registry(hkey, key, value_name, value):
    with winreg.OpenKey(hkey, key, 0, winreg.KEY_ALL_ACCESS) as key_handler:
        print(r"Starting creation of %s\%s" % (key, value_name))
        winreg.SetValueEx(key_handler, value_name, 0, winreg.REG_SZ, value)
        print(r"Successful creation of %s\%s" % (key, value_name))


def delete_registry(hkey, key, value_name):
    with winreg.OpenKey(hkey, key, 0, winreg.KEY_ALL_ACCESS) as key_handler:
        print(r"Starting deletion of %s\%s" % (key, value_name))
        winreg.DeleteValue(key_handler, value_name)
        print(r"Successful deletion of %s\%s" % (key, value_name))


def close_program(program_name):
    subprocess.call("TASKKILL /F /IM \"%s\"" % program_name, shell=True)


if __name__ == '__main__':
    main()