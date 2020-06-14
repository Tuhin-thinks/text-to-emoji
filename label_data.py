import re
import csv as cv
import os


def write_to_csv(filename, data):
    header = ['categories', 'topics', 'emojis']
    with open(filename, 'a', encoding='UTF-8') as csv_file:
        writer = cv.DictWriter(csv_file, header, lineterminator='\n')
        if os.stat(filename).st_size == 0:  # if file is created for first time
            writer.writeheader()  # write header
        writer.writerow(data)
    print('Successfully writen data to ', filename)


def analyze_line(line_string):
    try:
        data_dict = {}
        topic_regex_pattern = "; (\S*):"
        topic_regex_pattern_with_space = "\S\s{2}; (\S.*):"
        topic_regex = re.compile(topic_regex_pattern)
        topics = re.findall(topic_regex, line_string)
        if len(topics) == 0:
            topic_regex_whitespace = re.compile(topic_regex_pattern_with_space)
            topics = re.findall(topic_regex_whitespace, line_string)
        print(topics)
        data_dict['topics'] = ','.join(topics)  # storing in a dict

        # find the categories under each topic
        categories_regex_pattern = ': (\S.*)#'
        categories_regex = re.compile(categories_regex_pattern)
        categories = re.findall(categories_regex, line_string)
        # remove space from end of each word
        if len(categories) == 0:  # at some line ReGeX matching may fail
            alternate_category_pattern = '\S\s\s; (\S.*)#'  # one character followed by 2 spaces-followed by ';'-and another space
            alternate_category_regex = re.compile(alternate_category_pattern)
            categories = [word.strip() for word in re.findall(alternate_category_regex, line_string)]  # remove redundant spaces after each category
        categories = [word.strip() for word in categories]
        mod_category = [word.strip() for word in categories[0].split(',')]
        categories = mod_category
        print(categories)
        data_dict['categories'] = ','.join(categories)  # storing in a dict

        # emoji matching pattern
        emoji_regex_pattern = '\((.*)\)'
        emoji_regex = re.compile(emoji_regex_pattern)
        emojis = re.findall(emoji_regex, line_string)
        print(emojis)  # we need to get the unicode for the emojis
        data_dict['emojis'] = ','.join(emojis)

        write_to_csv(filename='Data_File.csv', data=data_dict)
    except IndexError:  # insufficient/incomplete data can cause index error(we expell those lines)
        print(f"Ignoring line: {line_string}")


def read_text_file(filename):
    count = 0
    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            if 30 <= count:
                print(count)
                analyze_line(line)
            count += 1
    print(f"Read {count} lines.")


read_text_file('emoji-zwj-sequences.txt')
