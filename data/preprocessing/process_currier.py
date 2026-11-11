# for the currier transliteration the format is structured as shown below:

#f1r:1 <%>VAS92.9FAE.AR.APAM.ZOE.ZOR9.QOR92.9.FOR.ZOE89
#f1r:2 2OR9.XAR.O.R.9.FAN.ZPAM.ZAR.AR?.QAR.QAR.8AD
#f1r:3 29AU.ZCF9.OR.9FAM.ZO8.QOAR9.Q?R.8ARAM.29

# we need to remove the line headers = f1r:1
# remove transcription annotation = <%>
# remove end of paragraph marker = <$>
# figure out how to handle unknown characters = ?

# keep actual transliterated text = VAS92...........
# keep digits 0-9, they are part of transliteration
# preserve word boundaries initially (.) = VAS92.9FAE.AR.APAM.ZOE.ZOR9.QOR92.9.FOR.ZOE89
# word boundaries will help with word lengths


import json
import re
from pathlib import Path


raw_currier = "data/raw_data/currier.jsonl"

pattern = r"^<%>|<\$>$"
processed_currier = []

with open(raw_currier, "r", encoding="utf-8") as file:
    for line in file:
        # converts file to python dictionary
        raw_text = json.loads(line)
        # we want raw_text[8]
        text = raw_text["text_raw"]

        processed_text = re.sub(pattern, "", text)
        processed_currier.append(processed_text)

output_path = "data/processed_data/processed_currier.json"
with open(output_path, "w", encoding="utf-8") as file:
    for line in processed_currier:
        file.write(line + "\n")

# for local testing
#for line in processed_currier[:3]:
    #print(line)

#for line in processed_currier:
    #if "<" in line or ">" in line:
        #print(line)
# this returns lines with <->
# need to figure out what <-> represents in the currier transliteration
