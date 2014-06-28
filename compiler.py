import os
import base64
import requests
from jinja2 import Template
from docutils.core import publish_parts

def make_html(rest):
    return publish_parts(rest, writer_name='html')['html_body']

def main():
    res = requests.get('https://api.github.com/repos/{user}/{repo}/readme'.format(
        user=os.environ['USER'],
        repo=os.environ['REPO']
        ))

    assert res.status_code == 200
    assert 'application/json' in res.headers['content-type']

    data = res.json()
    encoding = data['encoding']
    content = data['content']

    rst = make_html(base64.b64decode(content))
    with open('index.html') as handle:
        template = Template(handle.read())

    string = template.render(content=rst)
    with open('index.html', 'w') as handle:
        handle.write(string)

if __name__ == "__main__":
    main()
