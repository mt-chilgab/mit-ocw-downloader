from html.parser import HTMLParser
import urllib.request as urllib2
import re

def isListNotNull(l):
    if(l):
        return True
    else:
        return False

class CourseParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)

        # test attribute should remain constant for each CourseParser unless the site makes change
        self.testAttr = [('rel', 'coursePreview'), ('class', 'preview'), ]
        # stripping pattern, should remain constant
        self.pattern = re.compile(r'\s{2,}|\n\r\t')
        
        self.addAsCourse = False
        self.courseList = list(tuple())
        self.countEnd = int(0)

    # as course url is contained in start tag <a ...>, add url to collected data
    #
    #   COURSE INFO:
    #   ( url to course page, course number, course title, course level(undergraduate/graduate) )    
    #
    def handle_starttag(self, startTag, attrs):
        if(isListNotNull(attrs) & (startTag == 'a')):
            if(all(map(lambda i, j: i==j, attrs, self.testAttr))):
                self.addAsCourse = True            
                self.countEnd += 1
                if(self.countEnd == 1):
                    self.courseList.append((attrs[2][1], ))
            else:
                self.addAsCourse = False
        else:
            self.addAsCourse = False

    def handle_data(self, data):
        if(self.addAsCourse):
            data = self.pattern.sub('', data)
            if(data != ''):
                self.courseList[-1] += (data, )
            if(self.countEnd == 3):
                self.countEnd = 0
                self.addAsCourse = False

    def searchCourseNum(self, courseNum):
        resultList = list()
        i = 0
        for result in map(lambda j: True if j[1]==courseNum else False, self.courseList):
            if(result):
                resultList.append(i)
            i += 1
        return resultList



class HomepageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

        self.pattern = re.compile(r'\s{2,}|\n\r\t')
        self.addAsHome = (False, False)

        self.videoAvailable = bool()
        self.problemAvailable = bool()
        self.lectureNoteAvailable = bool()

        self.videoHomes = list(tuple())
        self.problemHomes = list(tuple())
        self.lectureNoteHomes = list(tuple())
    
    def handle_starttag(self, startTag, attrs):
        if(isListNotNull(attrs) & (startTag == 'ul')):
            if(attrs[0] == ('class', 'specialfeatures')):
                self.addAsHome = (True, False)
            else:
                self.addAsHome = (False, False)
    
        if(self.addAsHome[0] & (startTag == 'a')):
            if(attrs[0][0] == 'href'):
                self.addAsHome = (True, True)
                self.videoHomes.append((attrs[0][1],))
                self.problemHomes.append((attrs[0][1],))
                self.lectureNoteHomes.append((attrs[0][1],))
            else:
                self.addAsHome = (True, False)

    def handle_endtag(self, endTag):
        if(all(self.addAsHome) & (endTag == 'ul')):
            self.addAsHome = (False, False)

    def handle_data(self, data):
        if(all(self.addAsHome)):
            if(bool(re.match(r'#[Vv]ideo|[Vv]ideo', self.videoHomes[-1][0])) | bool(re.match(r'[Vv]ideo', data))):
                self.videoHomes[-1] = (data, self.videoHomes[-1][0])
            else:
                del self.videoHomes[-1]

            if(bool(re.match(r'[Ee]xam|[Aa]ssignment|[Pp]roblem', self.problemHomes[-1][0])) | bool(re.match(r'[Ee]xam|[Aa]ssignment|[Pp]roblem', data))):
                self.problemHomes[-1] = (data, self.problemHomes[-1][0])
            else:
                del self.problemHomes[-1]
            
            if(bool(re.match(r'[Ll]ecture\s[Nn]ote|[Ll]ecture-[Nn]otes', self.lectureNoteHomes[-1][0])) | bool(re.match(r'lecture-notes', data))):
                self.lectureNoteHomes[-1] = (data, self.lectureNoteHomes[-1][0])
            else:
                del self.lectureNoteHomes[-1]

    

#class PageParser(HTMLParser):
    
#    def __init__(self):
        

if __name__ == "__main__":
    print("Course Name?")
    courseName = input()
    coursePage = coursePage = urllib2.urlopen("https://ocw.mit.edu/courses/"+courseName)
    parser = CourseParser()
    parser.feed(str(coursePage.read().decode("UTF-8")))
    print(parser.courseList)
    
    print("Course Number?")
    classNum = input()
    print(parser.searchCourseNum(classNum))
    for res in parser.searchCourseNum(classNum):
        print(parser.courseList[res])

    print("Which one?")
    a = input()
    courseHomePage = courseHomePage = urllib2.urlopen("https://ocw.mit.edu"+parser.courseList[parser.searchCourseNum(classNum)[int(a)-1]][0])
    homeParser = HomepageParser()
    homeParser.feed(str(courseHomePage.read().decode("UTF-8")))
    print(homeParser.videoHomes, "\n")
    print(homeParser.problemHomes, "\n")
    print(homeParser.lectureNoteHomes, "\n")

