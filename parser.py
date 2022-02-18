from html.parser import HTMLParser
import urllib.request as urllib2
import re

class CourseParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)

        # test attribute should remain constant for each CourseParser unless the site makes change
        self.testAttr = [('rel', 'coursePreview'), ('class', 'preview'), ]
        # stripping pattern, should remain constant
        self.pattern = re.compile(r'\s{2,}|\n\r\t')
        
        self.courseList = list(tuple())
        self.countEnd = int(0)
        self.addAsCourse = False

    # as course url is contained in start tag <a ...>, add url to collected data
    #
    #   STANDARD COURSE INFO:
    #   ( url to course page, course number, course title, course level(undergraduate/graduate) )    
    #
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
        for result in map(lambda j: True if j[1]==courseNum else False, self.courseList):
            if(result):
                resultList.append(i)
            i += 1
        return resultList



class PageParser:

    # courseInfo should be formatted in STANDARD COURSE INFO
    def __init__(self, courseInfo):
        self.courseURL = "https://ocw.mit.edu"+courseInfo[0]
        self.videoAvailable = None
        self.videoLinks = None




if __name__ == "__main__":
    courseName = input()
    htmlPage = htmlPage = urllib2.urlopen("https://ocw.mit.edu/courses/"+courseName)
    
    parser = CourseParser()
    parser.feed(str(htmlPage.read().decode("UTF-8")))
    print(parser.courseList)
    
    classNum = input()
    handler = CourseHandler(parser.courseList)
    print(handler.searchCourseNum(classNum))
    for res in handler.searchCourseNum(classNum):
        print(parser.courseList[res])

