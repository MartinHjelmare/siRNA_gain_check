import sys
from lxml import etree
from collections import Counter

def add_gain(_channel, _channel_results, _detector):
    "This adds the gain value to a tuple for each channel."
    channel_tuple = _channel_results[_channel]
    channel_tuple = channel_tuple + (_detector.attrib['Gain'],)
    _channel_results[_channel] = channel_tuple
    return _channel_results

if len(sys.argv) != 2:
    print 'usage : siRNA_gain_check.py <path_to_XML_file> \nYou must specify the path to the XML file as the first arg'
    sys.exit(1)

path = sys.argv[1]

try:
    open(path, 'r')
except Exception:
    print "This file doesn't exist or can't be read from"
    sys.exit(1)

doc = etree.parse(path)
sequences = doc.findall("//ATLConfocalSettingDefinition")
green = ()
blue = ()
yellow = ()
red = ()
channel_results = {"Green": green, "Blue": blue, "Yellow": yellow, "Red": red}

for seq in sequences:
    LUTlist = seq.findall("LUT_List")
    LUTs = LUTlist[0].findall("LUT")
    DetectorList = seq.findall("DetectorList")
    detectors = DetectorList[0].findall("Detector")
    for detector in detectors:
        if (detector.attrib['IsActive'] == "1") & (detector.attrib['Gain'] != "0"):
            for lut in LUTs:
                if lut.attrib['Channel'] == detector.attrib['Channel']:
                    channel_results = add_gain(lut.attrib['LutName'], channel_results, detector)
# Counts how many values of each gain, each channel has, in a histogram fashion. Prints histogram from the Counter object.
for channel in channel_results:
    print(channel+": "+str(Counter(channel_results[channel]).items()))
