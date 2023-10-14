
# Author: Pierce Brooks

import re
import os
import sys
import json
import time
import emoji
import random
import subprocess
from PIL import Image
from pathlib import Path

prefix = os.getlogin().strip()
prefix = re.sub(r"\W+", "", prefix).upper()
descriptor = open(os.path.join(os.getcwd(), "packs.json"), "r")
content = descriptor.read()
descriptor.close()
packs = json.loads(content)
targets = []
descriptor = open(os.path.join(os.getcwd(), "emoji_autocomplete.json"), "r")
content = descriptor.read()
descriptor.close()
data = json.loads(content)
keys = list(data.keys())
extensions = []
extensions.append(".jpg")
extensions.append(".jpeg")

for root, folders, files in os.walk(os.getcwd()):
  for name in folders:
    if (name.startswith(".git")):
      continue
    targets.append(os.path.join(root, name))
  break

for target in targets:
  pack = os.path.basename(target)
  if not (pack in packs):
    continue
  print(pack+" = "+packs[pack])
  if (os.path.exists(os.path.join(target, prefix+pack.upper()+".def"))):
    continue
  for root, folders, files in os.walk(target):
    for name in files:
      for extension in extensions:
        if ((name.endswith(extension)) and not (os.path.exists(os.path.join(root, name+".png")))):
          image = Image.open(os.path.join(root, name))
          image.save(os.path.join(root, name+".png"))
          os.remove(os.path.join(root, name))
          break
    break
  for root, folders, files in os.walk(target):
    for name in files:
      if ((" " in name) or ("(" in name) or (")" in name)):
        image = Image.open(os.path.join(root, name))
        image.save(os.path.join(root, name.replace(" ", "_").replace("(", "_").replace(")", "_")))
        os.remove(os.path.join(root, name))
    break
  command = []
  command.append("pytgasu")
  command.append("prepare")
  command.append(target)
  print(str(command))
  print("Please now type \""+packs[pack]+"\", press enter, then type \""+prefix+pack.upper()+"\", and press enter once again.")
  lines = subprocess.check_output(command).decode().strip().split("\n")
  for line in lines:
    print(line.strip())
  time.sleep(1.0)
  if not (os.path.exists(os.path.join(target, prefix+pack.upper()+".def"))):
    print("Error: No definition file was generated!")
    sys.exit(0)
  descriptor = open(os.path.join(target, prefix+pack.upper()+".def"), "r")
  lines = descriptor.readlines()
  descriptor.close()
  content = []
  indices = []
  indices.append(len(keys))
  selections = 0
  for line in lines:
    line = line.strip()
    if (line.endswith("/")):
      index = len(keys)
      while not (index < len(keys)):
        index = random.randint(0, len(keys))
        if ((index in indices) or (emoji.emojize(data[keys[index]]["alpha_code"]) == data[keys[index]]["alpha_code"]) or (len(emoji.emojize(data[keys[index]]["alpha_code"])) > 1)):
          index = len(keys)
      indices.append(index)
      content.append(line+emoji.emojize(data[keys[index]]["alpha_code"]))
      selections += 1
      print(line+" = "+data[keys[index]]["alpha_code"]+" @ "+str(selections))
      continue
    content.append(line)
  descriptor = open(os.path.join(target, prefix+pack.upper()+".def"), "w", encoding="utf-8")
  for line in content:
    line += "\n"
    descriptor.write(line)
  descriptor.close()
  if (selections <= 0):
    print("Error: No emoji selections were made!")
    sys.exit(0)
  command = []
  command.append("pytgasu")
  command.append("upload")
  command.append("-s")
  command.append(os.path.join(target, prefix+pack.upper()+".def"))
  print(str(command))
  if not (os.path.exists(os.path.join(Path.home(), ".pytgasu", "asu.session"))):
    print("If this command execution seems significantly delayed, it is most likely waiting for you to submit your Telegram account's phone number and a security code.\nIn which case, please do type that in with the format \"+1XXXYYYZZZZ\" and then press enter.\nAfterwards, type in the security code that Telegram sends you and press enter again.\nYou must type in and enter the security code twice in a row, so do this for a second time.\nFinally, if there is a password activated on your Telegram account, then you should type that in followed by pressing enter once more.\nAs an alternative option, instead of doing all these actions without seeing the feedback ouput of the authentication system, you can kill this process with \"Ctrl+C\" and simply manually invoke \"pytgasu upload -s "+pack+"\" from your terminal.\nIf you choose this route, just launch this script again and it should pick where it left off.")
  lines = subprocess.check_output(command).decode().strip().split("\n")
  for line in lines:
    print(line.strip())
  break
