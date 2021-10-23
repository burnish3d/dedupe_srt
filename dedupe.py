import re
import os
from dataclasses import dataclass
import argparse



empty_or_line_number_regex = r"^$|^\d+$"
regex = r"\d+\n(\d+:\d+:\d+,\d+\s-->\s\d+:\d+:\d+,\d+)\n(.*)" #matches the subtitle number, captures time range and content
files = [elem for elem in os.listdir() if elem.endswith(".srt")]
target_dir = "./deduped_srt/"
timerange_regex = r"\d+:\d+:\d+,\d+\s-->\s\d+:\d+:\d+,\d+"
try:
  os.mkdir(target_dir)
except FileExistsError:
  pass

@dataclass
class Subtitle:
  number: int
  timerange: str = ""
  content: str = ""
  
  def __str__(self):
    return f"{self.number}\n{self.timerange}{self.content}"

for file in files:
  with open(file,"r") as f, open(f"{target_dir}{file}","w") as dedupe:
    #draw out first subtitle, if error checking or validation needs to occur we can do it here
    first_count = int(f.readline())
    first_timerange = f.readline()
    first_content = f.readline()
    sub = Subtitle(number=first_count, timerange=first_timerange, content=first_content)
    line = f.readline()
    #if there are multiple subtitles in the first one grab them too
    while not re.match(empty_or_line_number_regex, line):
      sub.content += '\n' + line
    #we should start this loop with line representing an empty line
    while line:
      if re.match(timerange_regex, line):
        if line != sub.timerange: #we have found a new timestamp and need to write our now finished subtitle and start making a new one
          dedupe.write(str(sub) + '\n')
          sub = Subtitle(number=sub.number+1, timerange=line, content=f.readline()) #there is always at least one line in a subtitle
      elif re.match(empty_or_line_number_regex,line):
        pass
      else:
        sub.content += line
      line = f.readline()
    
    #on exit we should flush the last sub out
    dedupe.write(str(sub))