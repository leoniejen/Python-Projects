"""
File: babynames.py
Name: Leonie
--------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import sys


def add_data_for_name(name_data, year, rank, name):
    """
    Adds the given year and rank to the associated name in the name_data dict.

    Input:
        name_data (dict): dict holding baby name data, e.g. name_data = {'Kylie': {'2010': '57'}, 'Nick': {'2010': '37'}}
        year (str): the year of the data entry to add
        rank (str): the rank of the data entry to add
        name (str): the name of the data entry to add

    Output:
        This function modifies the name_data dict to store the provided
        name, year, and rank. This function does not return any value.
    """
    # name is not in dict yet
    if name not in name_data:
        name_data[name] = {year: rank}
    # name is in dict
    else:
        for listed_name, listed_data in name_data.items():
            # restrict to the current name user entered
            if name == listed_name:
                # situation: in the same year, a name both scored  in female's and male's rank, save the topper rank
                if year in listed_data:
                    if int(rank) < int(listed_data[year]):
                        listed_data[year] = rank
                # situation: the name is on the rank in different years, add to listed_data
                else:
                    name_data[name][year] = rank


def add_file(name_data, filename):
    """
    Reads the information from the specified file and populates the name_data
    dict with the data found in the file.

    Input:
        name_data (dict): dict holding baby name data
        filename (str): name of the file holding baby name data

    Output:
        This function modifies the name_data dict to store information from
        the provided file name. This function does not return any value.
    """
    with open(filename, 'r') as f:
        year_data = []
        for line in f:
            tokens = line.split()  # Remove blank spaces, output type: list
            tokens = ''.join(tokens)  # output type: str
            tokens = tokens.split(',')  # split str by comma, output type: list
            year_data.append(tokens)  # data structure of year_data: lists in a list
        for data in year_data[1:]:
            year = ''.join(year_data[0])
            rank = data[0]
            for i in range(len(data)-1):  # except rank, the rest of data(list) are names we need, thus len(data)-1
                name = data[i+1]
                # print(f'year, rank, name: {year} / {name} / {rank}')
                add_data_for_name(name_data, year, rank, name)


def read_files(filenames):
    """
    Reads the data from all files specified in the provided list
    into a single name_data dict and then returns that dict.

    Input:
        filenames (List[str]): a list of filenames containing baby name data

    Returns:
        name_data (dict): the dict storing all baby name data in a structured manner
    """
    name_data = {}
    for filename in filenames:
        add_file(name_data, filename)
    return name_data


def search_names(name_data, target):
    """
    Given a name_data dict that stores baby name information and a target string,
    returns a list of all names in the dict that contain the target string. This
    function should be case-insensitive with respect to the target string.

    Input:
        name_data (dict): a dict containing baby name data organized by name
        target (str): a string to look for in the names contained within name_data

    Returns:
        matching_names (List[str]): a list of all names from name_data that contain
                                    the target string
    """
    matching_names = []
    for name, data in name_data.items():
        name_substring_list = []  # empty list, save substrings for names
        if len(target) <= len(name):  # increase performance, ignore names that its length are longer than target's
            for i in range(len(name)-len(target)+1):
                substring = ''.join(name)[i:i+len(target)]  # substring's length == target's length, output type = str
                name_substring_list.append(substring)
            is_listed = False  # switch for making sure a name only appear once
            for name_substring in name_substring_list:
                if not is_listed:
                    if target.upper() == name_substring.upper():  # .upper(), case sensitive
                        is_listed = True  # switch is_listed to true
                        matching_names.append(name)
    return matching_names


def print_names(name_data):
    """
    (provided, DO NOT MODIFY)
    Given a name_data dict, print out all its data, one name per line.
    The names are printed in alphabetical order,
    with the corresponding years data displayed in increasing order.

    Input:
        name_data (dict): a dict containing baby name data organized by name
    Returns:
        This function does not return anything
    """
    for key, value in sorted(name_data.items()):
        print(key, sorted(value.items()))


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # Two command line forms
    # 1. file1 file2 file3 ..
    # 2. -search target file1 file2 file3 ..

    # Assume no search, so list of filenames to read
    # is the args list
    filenames = args

    # Check if we are doing search, set target variable
    target = ''
    if len(args) >= 2 and args[0] == '-search':
        target = args[1]
        filenames = args[2:]  # Update filenames to skip first 2

    # Read in all the filenames: baby-1990.txt, baby-2000.txt, ...
    names = read_files(filenames)

    # Either we do a search or just print everything.
    if len(target) > 0:
        search_results = search_names(names, target)
        for name in search_results:
            print(name)
    else:
        print_names(names)


if __name__ == '__main__':
    main()
