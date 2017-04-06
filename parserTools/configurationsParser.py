import re
from parserTools.cleaner import *
regexConfigurationVariables = r"{(.*),(.*),(.*)}"

def parseConfigurationVariables(text, configs, types):
    matches = re.finditer(regexConfigurationVariables, text, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        tempConfig = [] #0 -> name 1 -> value, 2 -> type    
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            tempConfig.append(match.group(groupNum))
        tempConfig[1] = removeQuotes(tempConfig[1])
        if not tempConfig[1] in types.keys():
            print("ERROR - Failed to apply configuration variable (INVALID TYPE): number %d, name: %s, type: %s" % (matchNum, tempConfig[0], tempConfig[2]))
        else:
            configs[tempConfig[0]] = types[tempConfig[1]](tempConfig[2]) #cast to type
    return configs