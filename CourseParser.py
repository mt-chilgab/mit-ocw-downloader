from html.parser import HTMLParser
import urllib.request as urllib2
import re

class CourseParser(HTMLParser):
    #initializing course list
    courseList = list(tuple())
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
                    self.courseList.append((attrs[2][1], ))
        else:
            self.addAsCoruse = False

    def handle_data(self, data):
        if(self.addAsCourse):
            data = self.pattern.sub('', data)
            if(data != ''):
                self.courseList[-1] += (data, )
            if(self.countEnd == 3):
                self.countEnd = 0
                self.addAsCourse = False


class CourseHandler:

    def __init__(self, courseList):
        self.courseList = courseList
        self.courseCard = len(courseList)

    def searchCourseNum(self, courseNum):
        resultList = list()
        i = 0
        for result in list(map(lambda j: True if j[1]==courseNum else False, self.courseList)):
            if(result):
                resultList.append(i)
            i += 1
        return resultList




#creating overriden course parser and feeding it with urllib2
parser = CourseParser()
course = input()
html_page = html_page = urllib2.urlopen("https://ocw.mit.edu/courses/"+course+"/")
parser.feed(html_page.read().decode("UTF-8"))

#course search test
num = input()
ch = CourseHandler(parser.courseList)
print(ch.searchCourseNum(num))
for course in ch.searchCourseNum(num):
    print(parser.courseList[course])

