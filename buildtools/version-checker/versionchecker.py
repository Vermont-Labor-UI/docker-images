import json
from packaging import version
import re
import sys

def load_banned_versions():
    with open("bannedversions.json") as f:
        return json.load(f)

def load_project_assets(project_file):
    print("Loading %s" % project_file)
    with open(project_file) as f:
        return json.load(f)

def check_target_version(target):
    target_array = target.split(',')
    if target_array[0] == '.NETCoreApp':
        m = re.search(r'Version=v(.*)', target_array[1])
        target_version = m.group(1)
        if version.parse(target_version) >= version.parse("2.2"):
            raise("\tTarget %s is invalid.  We do not support anything greater than or equal to 2.2" % target_version)
        else:
            print("\tTarget %s is valid." % target_version)


def check_dependency(dependency, semversion, banned_versions):
    if dependency in banned_versions:
        banned = banned_versions[dependency]
        banned_semversion = version.parse(banned["Version"])
        if banned["MustBe"] == "LessThan":
            if semversion < banned_semversion:
                return {
                    "message" : "\t\tDependency %s(%s) Passed.  Must be less than %s" % (dependency, semversion, banned["Version"]),
                    "passed" : True
                }
            else:
                return {
                    "message" : "\t\tDependency %s(%s) Failed.  Must be less than %s" % (dependency, semversion, banned["Version"]),
                    "passed" : False
                }
    return {
        "message" : "\t\tDependency %s not banned" % (dependency),
        "passed" : True
    }

def check_package(packageKey, package, banned_versions):
    package_array = packageKey.split("/")
    package_name = package_array[0]
    package_version = package_array[1]
    passed = check_dependency(package_name, version.parse(package_version), banned_versions)
    error_messages = []
    if not passed:
        return
    if "dependencies" in package:
        for dependency in package["dependencies"]:
            check_resposne = check_dependency(dependency, version.parse(package["dependencies"][dependency]), banned_versions)
            if check_resposne["passed"] == False:
                print("\tBanned Version Found in %s (%s)" % (package_name, package_version))
                print(check_resposne["message"])
                error_messages.append(check_resposne["message"])
    
    return error_messages

def find_banned_versions(project_assets, banned_versions):
    if "targets" not in project_assets:
        raise("Unable to get targets from project assets")
    targets = project_assets["targets"]
    error_messages = []
    for targetKey in targets:
        check_target_version(targetKey)

        for package in targets[targetKey]:
            error_messages = error_messages + check_package(package, targets[targetKey][package], banned_versions)

    return error_messages


if __name__ == "__main__":
    banned_versions = load_banned_versions()
    project_assets = load_project_assets(sys.argv[1])
    #print(banned_versions)
    #print(project_assets)
    print("Checking for banned versions")
    error_messages = find_banned_versions(project_assets, banned_versions)
    if len(error_messages) > 0:
        print("=====\nBanned Packages Found\n=====")
        exit(1)
    exit(0)
    
    