# Publish to Medium

Medium now has an API which allows users to publish posts. This is a small
Python script which will allow you to write posts in Markdown and then upload
them to Medium where you can review them as a draft.

## Usage
1. Go to your [Medium Settings](https://medium.com/me/settings) and create an
	 Integration Token
2. Create a `.env` file with your integration token
```
MEDIUM_INTEGRATION_TOKEN=<your integration token here>
```
3. Create a markdown file with your article
4. Run the script
```
usage: publish_draft.py [-h] --title TITLE [--tags [TAGS ...]] filepath

positional arguments:
  filepath           Path to markdown file

optional arguments:
	-h, --help         show this help message and exit
	--title TITLE      The title of the work
	--tags [TAGS ...]  Tags (Maximum of 3)
```

## Images
Medium will handle remote images. They can be placed in either a <img> tag or
the standard markdown image syntax `![alt text](url "caption")`.

For local images, they will be uploaded to Medium, and the markdown source will
be updated the URL of the image on Medium. In order for the script to detect
local images, they must be placed using the standard image syntax `![alt
text](url "caption")`. If the image does not match this format, it will not be
uploaded to Medium.
