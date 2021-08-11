#!/usr/local/bin/python3

import os
import argparse
import requests
import sys

from dotenv import load_dotenv
load_dotenv()

MEDIUM_API_USER_URL = "https://api.medium.com/v1/me"
MEDIUM_API_IMAGE_URL = "https://api.medium.com/v1/images"
TOKEN = os.getenv("MEDIUM_INTEGRATION_TOKEN")

def authenticate():
  print("Authenticating user")
  headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {TOKEN}" }
  res = requests.get(MEDIUM_API_USER_URL, headers=headers)
  res.raise_for_status()
  data = res.json()["data"]
  return data["id"], data["url"]

def publish(author_id, title, content, tags=[]):
  headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {TOKEN}" }
  url = f"https://api.medium.com/v1/users/{author_id}/posts"
  payload = {
    "title": title,
    "contentFormat": "markdown",
    "publishStatus": "draft",
    "tags": tags,
    "content": content
  }

  res = requests.post(url, json=payload, headers=headers)
  res.raise_for_status()
  return res

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

user_id, user_url = authenticate()
with open(args.filepath) as f:
  publish(user_id, args.title, f.read(), tags=args.tags)
print(f"Successfully uploaded draft \"{args.title}\". Visit {user_url} to review it")

