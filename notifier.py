from lxml import html
import requests

page = requests.get('http://results.unipune.ac.in/')
tree = html.fromstring(page.content)

#get text from first row
first = tree.xpath('//table[@class="table"]//tr[2]//text()')




