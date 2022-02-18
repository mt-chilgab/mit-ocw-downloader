from html.parser import HTMLParser
import urllib.request as urllib2
import re

class CourseParser(HTMLParser):
    #initializing course list
    listsCourse = list(tuple())
    countEnd = 0
    addAsCourse = False

    #testAttr should remain constant, until the site makes change
    testAttr = [('rel', 'coursePreview'), ('class', 'preview'), ]
    #stripping pattern, should remain constant
    pattern = re.compile(r'\s{2,}|\n\r\t')

    def handle_starttag(self, startTag, attrs):
        if(startTag == 'a'):
            if(all(map(lambda i, j: i==j, attrs, self.testAttr))):
                self.addAsCourse = True            
                self.countEnd += 1
                if(self.countEnd == 1):
                    self.listsCourse.append((attrs[2][1], ))
        else:
            self.addAsCoruse = False

    def handle_data(self, data):
        if(self.addAsCourse):
            data = self.pattern.sub('', data)
            if(data != ''):
                self.listsCourse[-1] += (data, )
            if(self.countEnd == 3):
                self.countEnd = 0
                self.addAsCourse = False


#Creating overriden course parser and feeding it with urllib2
parser = CourseParser()
course = input()
html_page = html_page = urllib2.urlopen("https://ocw.mit.edu/courses/"+course+"/")
parser.feed(html_page.read().decode("UTF-8"))

#Printing the extracted course infos
print(parser.listsCourse)
print("\n\n", len(parser.listsCourse))
