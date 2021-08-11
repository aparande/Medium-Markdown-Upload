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
Currently, the script does not support uploading images on your local machine to
Medium. However, remote images can be included by using a "<img>" tag in your
Markdown.
