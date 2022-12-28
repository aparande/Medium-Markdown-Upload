#!/usr/local/bin/python3

import argparse
import re
import shutil
import sys

import api

# MULTILINE allows the regex to transcend lines. DOTALL means . matches a newline
IMAGE_REGEX = re.compile(r"!\[(.*?)\]\((.*?) (\"(.*?)\")?\)", re.MULTILINE | re.DOTALL)

def sub_url(img_match: re.Match, dry_run: bool = False, verbose: bool = False):
  image_path = img_match.group(2)

  if "http" in image_path:
    # Ignore remote images. Medium will handle them
    return img_match.group(0)

  if dry_run or verbose:
    print(f"Alt Text: {img_match.group(1)}, URL: {image_path}, Caption:\
        {img_match.group(3)}")

  image_url = 'http://cdn.medium.com/really-long-url-that-might-break-regex' if dry_run else api.upload_image(image_path)

  caption_no_lines = img_match.group(3).replace("\n", "")
  return f"[{img_match.group(1)}]({image_url} {caption_no_lines})"

def process(path, dry_run: bool = False, verbose: bool = False):
  with open(path, 'r') as f:
    content = f.read()

  content = IMAGE_REGEX.sub(lambda x: sub_url(x, dry_run=dry_run,
    verbose=verbose), content)
  for img_match in IMAGE_REGEX.finditer(content):
    image_path = img_match.group(2)

    if "http" not in image_path:
      if dry_run or verbose:
        print(f"Alt Text: {img_match.group(1)}, URL: {image_path}, Caption:\
            {img_match.group(3)}")

      image_url = 'http://cdn.medium.com/really-long-url-that-might-break-regex' if dry_run else api.upload_image(image_path)
      start, end = img_match.start(2), img_match.end(2)

      if verbose:
        print(f"Replacing {content[start:end]} with {image_url}")

      content = content[:start] + image_url + content[end:]
    else:
      # Ignore remote images. Medium will handle them
      continue

  shutil.copyfile(path, f"{path}.bkp")
  with open(path, 'w') as f:
    f.write(content)


argparser = argparse.ArgumentParser()
argparser.add_argument("--title", dest="title", type=str,
    required=True, help="The title of the work")
argparser.add_argument("--tags", dest="tags", nargs="*",
    default=[], help="Tags (Maximum of 3)")
argparser.add_argument("--dry-run", action='store_true', help="Whether to\
  actually do the upload or not")
argparser.add_argument("--verbose", action='store_true', help="Whether to print\
debug info to the console")
argparser.add_argument("filepath", type=str, help="Path to markdown file")

args = argparser.parse_args()

if len(args.tags) > 3:
  print("Articles can only be posted with a maximum of 3 tags")
  sys.exit(1)

user_id, user_url = api.authenticate()
process(args.filepath, dry_run=args.dry_run, verbose=args.verbose)
if not args.dry_run:
  with open(args.filepath) as f:
    api.publish(user_id, args.title, f.read(), tags=args.tags)
  print(f"Successfully uploaded draft \"{args.title}\". Visit {user_url} to review it")

