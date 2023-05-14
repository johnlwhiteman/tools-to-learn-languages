import pandas as pd
import re
import sys
import xml.dom.minidom
from pprint import pprint as pp

def formatTs(ts):
    return int(ts.replace("t", ""))

def hasSentenceLowerCase(token):
    return re.search('[a-z]', token)

def read(path):
    with open(path, "r", encoding="utf-8") as fd:
        return fd.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as fd:
        return fd.write(content)

def extract(path):
    transcript = []
    content = read(path)
    content = content.replace("<br/>", " ").replace("</span>", "")
    for i in range(0, 100):
        x = f"style=\"style{i}\""
        content = content.replace(x, "").replace("<span >", "")
    doc = xml.dom.minidom.parseString(content)
    e = doc.getElementsByTagName("div")
    if len(e) != 1 or not e[0].hasAttribute("xml:space"):
        sys.exit("Bad things for good people.")
    for p in e[0].getElementsByTagName("p"):
        tmp = {
            "id":  p.getAttribute("xml:id"),
            "begin": formatTs(p.getAttribute("begin")),
            "end": formatTs(p.getAttribute("end")),
            "text": ""
        }
      #  s = p.getElementsByTagName("span")
      #  if len(s) > 0:
      #      for i, ss in enumerate(s):
           #     tmp["text"] = f"{tmp['text']} {ss.firstChild.data}"
      #  else:
        tmp["text"] = p.firstChild.data
        tmp["text"] = re.sub('(\-|\- )', "", tmp["text"])
        tmp["text"] = tmp["text"].replace("-[", "[").strip()
        tmp["text"] = tmp["text"].replace("  ", " ").strip()
        lMatch = re.search(r'\[', tmp["text"])
        rMatch = re.search(r'\]', tmp["text"])
        while lMatch and rMatch:
            s = tmp["text"][lMatch.start():rMatch.start() + 1]
            tmp["text"] = tmp["text"].replace(s, "").strip()
            lMatch = re.search(r'\[', tmp["text"])
            rMatch = re.search(r'\]', tmp["text"])
        if len(tmp["text"]) > 0 and re.search('[a-z]', tmp["text"]):
            if not re.search('♪', tmp["text"]):
                transcript.append(tmp)
    return transcript

def try2MapThings(t1, t2):
    with open("transcript.txt", "w", encoding="utf-8") as fd:
        for i, line in enumerate(t1):
            if i >= len(t2):
                break
            fd.write(f"{t1[i]['text']}\n")
            fd.write(f"{t2[i]['text']}\n")
            fd.write("----------------\n")

def try2MatchByTime(t1, t2):
    i = 0
    df1 = pd.DataFrame(t1)
    df2 = pd.DataFrame(t2)
    with open("map-by-time.txt", "w", encoding="utf-8") as fd:
        for index, row in df1.iterrows():
            df = df2[(row["begin"] <= df2["begin"]) & (df2["end"] <= row["end"])]
            if len(df) == 1:
                fd.write(f"{row['text']}\n")
                fd.write(f"{df['text'].values[0]}\n")
                fd.write("----------------\n")
                i += 1
    print(f"Map Success: {i / len(df1) * 100:.2f}%")


#if len(sys.argv) != 2:
 #   sys.exit("What the heck? Provide two language XML files")
transcripts = []
t1 = extract(sys.argv[1])
t2 = extract(sys.argv[2])
try2MapThings(t1, t2)
print(len(t1))
print(len(t2))
#try2MatchByTime(df1, df2)
