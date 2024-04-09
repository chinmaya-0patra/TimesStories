
import urllib.request
from html.parser import HTMLParser
import json
class TimeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_story_container = False
        self.inside_a = False
        self.stories = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and 'homepage-module' in value:
                    self.inside_story_container = True
        elif tag == 'a' and self.inside_story_container:
            self.inside_a = True
            for name, value in attrs:
                if name == 'href' and value.startswith('/'):
                    self.stories.append({'title': '', 'link': value})

    def handle_data(self, data):
        if self.inside_a:
            self.stories[-1]['title'] += data

    def handle_endtag(self, tag):
        if tag == 'div' and self.inside_story_container:
            self.inside_story_container = False
        elif tag == 'a' and self.inside_a:
            self.inside_a = False

def get_latest_stories():
    url = 'https://time.com'
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    parser = TimeHTMLParser()
    parser.feed(html)
    parser.close()

    return parser.stories[:6]

if __name__ == "__main__":
    latest_stories = get_latest_stories()
    
    # Write the JSON data to a file
    with open('time_stories.json', 'w') as json_file:
        json.dump(latest_stories, json_file, indent=2)
        
    print("JSON file saved as 'time_stories.json'")
    print(latest_stories)