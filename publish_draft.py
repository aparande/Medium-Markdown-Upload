#!/usr/local/bin/python3

import sys
import argparse
import re
import api

# MULTILINE allows the regex to transcend lines. DOTALL means . matches a newline
IMAGE_REGEX = re.compile(r"!\[(.*?)\]\((.*?) (\"(.*?)\")?\)", re.MULTILINE | re.DOTALL)

def process(path):
  with open(path, 'r') as f:
    content = f.read()

  for match in IMAGE_REGEX.finditer(content):
    image_path = match.group(2)

    # Ignore remote images. Medium will handle them
    if "http" not in image_path:
      image_url = api.upload_image(image_path)
      start, end = match.start(2), match.end(2)
      content = content[:start] + image_url + content[end:]

  with open(path, 'w') as f:
    f.write(content)


argparser = argparse.ArgumentParser()
argparser.add_argument("--title", dest="title", type=str,
    required=True, help="The title of the work")
argparser.add_argument("--tags", dest="tags", nargs="*",
    default=[], help="Tags (Maximum of 3)")
argparser.add_argument("filepath", type=str, help="Path to markdown file")

args = argparser.parse_args()

if len(args.tags) > 3:
  print("Articles can only be posted with a maximum of 3 tags")
  sys.exit(1)

user_id, user_url = api.authenticate()
process(args.filepath)
with open(args.filepath) as f:
  api.publish(user_id, args.title, f.read(), tags=args.tags)
print(f"Successfully uploaded draft \"{args.title}\". Visit {user_url} to review it")

