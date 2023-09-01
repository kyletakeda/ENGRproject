# This script will parse the xml File provided by SUMO
# using fcd-output

# from geopy.distance import distance as dist
import re
from math import pi, log10
carCount = input("Enter car count from simulation: ")
filename = "Test.txt"
carFiles = [None] * int(carCount)

c = 299792458  # speed of light in a vacuum, approx. air
wavelen = c/(5.89e9)  # wavelength at C-V2X 5.89GHz carrier

# Gets the offset of the of the cords start and end location in a string
def ParseOffset(contents, match):
    offset = 1
    while contents[match.end() + offset].isdigit() or contents[match.end() + offset] == '.':
        offset += 1
    return offset

def GenerateFiles():
    for i in range(int(carCount)):
        temp = open("Car"+str(i)+"Pos.txt", 'w')
        for x in range(5):
            temp.write("\n")  # setting line length of new file
        carFiles[i] = "Car"+str(i)+"Pos.txt"
        temp.close()
        print(carFiles)

def GatherCarPositions(CarID, carNumber):
    # gather file length
    f = open(filename, 'r')
    x = len(f.readlines())
    f.close()

    # gather locations from file that should be parsed
    f = open(filename, 'r')
    writeFile = open(carFiles[carNumber], 'r')  # Ignore this warning (due to the fact that I fill the list after initialization)
    data = writeFile.readlines()
    for i in range(x):
        temp = f.readline()
        # search for if the current line has the Cars ID anywhere on the line, if so we get the cords from it
        if re.search('vehicle id="{}"'.format(CarID), temp):
            for match in re.finditer('x="', temp):  # get the index on the string where the the x-cord starts
                offset = ParseOffset(temp, match)
                # writeFile.write(temp[match.end():match.end()+offset] + " ")
                data[1] = data[1] + temp[match.end():match.end()+offset] + ", "  # write the cord to the 2th line

        if re.search('vehicle id="{}"'.format(CarID), temp):
            for match in re.finditer('y="', temp):  # get the index on the string where the the y-cord starts
                offset = ParseOffset(temp, match)
                data[4] = data[4] + temp[match.end():match.end()+offset] + ", "  # write the cord to the 4th line

    data[1] = data[1] + "\n"
    data[4] = data[4] + "\n"
    data[0] = "Car " + str(carNumber) + " x_Position: "
    data[3] = "Car " + str(carNumber) + " y_Position: "

    writeFile.close()
    with open(carFiles[carNumber], 'w') as file:  # Ignore this warning (due to the fact that I fill the list after initialization)
        file.writelines(data)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GenerateFiles()
    # in the xml file you have the cars ID's (labeled vehicle ID)
    # the id is the first parameter inputed to the car position function
    # the second parameter is the index of the car in the list generated in the generate cars function
    # 0 refers to car 0, 1 refers to car 1
    # the number is just preference and 0 corresponds to car0pos.txt (post-file creation)
    GatherCarPositions("Fast", 0)
    GatherCarPositions("Slow", 1)


