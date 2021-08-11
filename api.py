import os
import sys
import requests
from requests_toolbelt import MultipartEncoder

from dotenv import load_dotenv
load_dotenv()


MEDIUM_API_USER_URL = "https://api.medium.com/v1/me"
MEDIUM_API_IMAGE_URL = "https://api.medium.com/v1/images"
IMAGE_FILETYPES = {
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".png": "image/png",
  ".gif": "image/gif",
  ".tiff": "image/tiff"
}

TOKEN = os.getenv("MEDIUM_INTEGRATION_TOKEN")

def authenticate(token=TOKEN):
  print("Authenticating user")
  headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {token}" }
  res = requests.get(MEDIUM_API_USER_URL, headers=headers)
  res.raise_for_status()
  data = res.json()["data"]
  return data["id"], data["url"]

def publish(author_id, title, content, tags=[], token=TOKEN):
  headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {token}" }
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

def upload_image(image_path, token=TOKEN):
  print(f"Uploading image {image_path}")
  # Get image attributes
  filename = os.path.basename(image_path)
  _, extension = os.path.splitext(image_path)
  if extension not in IMAGE_FILETYPES:
    print(f"{image_path} is not a valid image. Medium only exists jpeg, png, gif, and tiff")
    print("Aborting upload")
    sys.exit(1)
  content_type = IMAGE_FILETYPES[extension]

  # Construct and Execute the request
  payload = { "image": (filename, open(image_path, 'rb'), content_type) }
  encoder = MultipartEncoder(payload, boundary="FormBoundaryXYZ")
  headers = { 'Authorization': f"Bearer {token}", 'Content-Type': encoder.content_type }
  res = requests.post(MEDIUM_API_IMAGE_URL, data=encoder.to_string(), headers=headers)
  res.raise_for_status()
  return res.json()["data"]["url"]

