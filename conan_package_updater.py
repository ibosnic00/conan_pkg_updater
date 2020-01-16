import sys
import getopt
import argparse
import os


def parse_args():
    """ Parsed command line arguments """
    parser = argparse.ArgumentParser(
        description="Program used for preparing CONAN package")
    parser.add_argument(
        "--server_version_file_path", default=False, help="activate if C++ server version is to be changed")
    parser.add_argument(
        "--new_version", help="new version of project (MAJOR.MINOR.PATCH)")

    return parser.parse_args()


def change_string_in_line(file_name, line_beggining, new_string, sign_prior_to_old_string, sign_after_old_string):
    """ Searchs for line that begins with {line_beggining} in {file_name} and then replaces string located between 
    {sign_prior_to_old_string} and {sign_after_old_string} with {new_string} """
    f = open(file_name, "r+")
    line_to_find = line_beggining
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith(line_to_find):
            version_start = i.find(sign_prior_to_old_string) + \
                len(sign_prior_to_old_string)
            version_end = i.rfind(sign_after_old_string)
            new_line = i[:version_start] + new_string + i[version_end:]
            f.write(new_line)
            print('\nReplaced line: {i}with {new_line}in file "{file_name}"'.format(
                **locals()))
        else:
            f.write(i)
    f.truncate()
    f.close()


def update_version_in_conanfile(file_name, new_version):
    """ Searchs for version in conanfile.py """
    f = open(file_name, "r+")
    line_to_find = '    version ='
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith(line_to_find):
            version_start = i.find('"') + len('"')
            version_end = i.rfind('"')
            new_line = i[:version_start] + new_version + i[version_end:]
            f.write(new_line)
            print('\nReplaced line: {i}with {new_line}in file "{file_name}"\n'.format(
                **locals()))
        else:
            f.write(i)
    f.truncate()
    f.close()


def parse_version(version):
    """ Parses version arguments and checks if format is ok"""
    parsed_version = {"major": 0, "minor": 0, "patch": 0}
    if (version.count('.') != 2):
        print("Wrong version format. Should be MAJOR.MINOR.PATCH")
        return -1
    start = version.find('.')
    end = version.rfind('.')
    parsed_version["major"] = version[:start]
    parsed_version["minor"] = version[start+1:end]
    parsed_version["patch"] = version[end+1:]
    return parsed_version


def update_version_in_cmakelists(file_name, new_version):
    """ Searchs for version in CMakeLists.txt """
    f = open(file_name, "r+")
    line_to_find = 'project('
    string_prior_to_version = 'VERSION'
    string_after_version = 'DESCRIPTION'
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith(line_to_find):
            version_start = i.find(string_prior_to_version) + \
                len(string_prior_to_version) + len(' ')
            version_end = i.find(string_after_version) - len(' ')
            new_line = i[:version_start] + new_version + i[version_end:]
            f.write(new_line)
            print('\nReplaced line: {i}with {new_line}in file "{file_name}"\n'.format(
                **locals()))
        else:
            f.write(i)
    f.truncate()
    f.close()


def main():
    """ Main scheduler """
    parsed_args = parse_args()
    project_path = os.path.dirname(os.path.abspath(__file__))
    parsed_version = parse_version(parsed_args.new_version)
    if (parsed_version != -1):
        conanfile_location = os.path.join(project_path, "conanfile.py")
        update_version_in_conanfile(
            conanfile_location, parsed_args.new_version)
        cmakelists_location = os.path.join(project_path, "CMakeLists.txt")
        update_version_in_cmakelists(
            cmakelists_location, parsed_args.new_version)
        if (parsed_args.server_version_file_path):
            print("Parsed version: " + str(parsed_version))
            server_file_path = os.path.join(
                project_path, parsed_args.server_version_file_path)
            change_string_in_line(server_file_path, "      major", parsed_version["major"], "{","}")
            change_string_in_line(server_file_path, "      minor", parsed_version["minor"], "{","}")
            change_string_in_line(server_file_path, "      patch", parsed_version["patch"], "{","}")
    else:
        print("Modify version and try again.")


main()
