import re
from datetime import datetime


class Message:
    def __init__(self, xml):
        self.category = []
        for data in xml:
            if data.tag == 'title':
                self.title = data.text
            elif data.tag == 'link':
                self.link = data.text
            elif data.tag == 'description':
                self.description = re.sub(r"\<.*\>", "", data.text)
            elif data.tag == 'category':
                self.category.append(data.text)
            elif data.tag == 'pubDate':
                self.pubDate = datetime.strptime(
                    data.text, '%a, %d %b %Y %H:%M:%S %Z')

    def to_message(self):
        return '%s\nPublication date: %s\n\nIssue: %s\nTags: %s\n\n%s\n' % (self.title,
                                                                            self.pubDate,
                                                                            self.description,
                                                                            ' '.join(
                                                                                ['#%s' % x for x in self.category]),
                                                                            self.link)
