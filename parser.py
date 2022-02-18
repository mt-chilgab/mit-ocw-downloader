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
    

    # pages with video, problem(exam, assignments, problems), lecture notes will be listed.
    #
    # self.videoHomes -> [(title of page, page url), (title of page 2, page url 2), ...]
    # self.problemHomes -> same as above
    # self.lectureNoteHomes -> same as above
    #
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
            else:
                self.addAsHome = (True, False)

    def handle_endtag(self, endTag):
        if(all(self.addAsHome) & (endTag == 'ul')):
            self.addAsHome = (False, False)

    def handle_data(self, data):
        if(all(self.addAsHome)):
            data = self.pattern.sub('', data)

            # used & because some lectures provide with captions: video and caption link lead to the same page
            if(bool(re.search(r'video', self.videoHomes[-1][0])) | bool(re.search(r'[Vv]ideo', data))):
                self.videoHomes[-1] = (data, self.videoHomes[-1][0])
            elif(bool(re.search(r'(exam|assignment|problem)', self.videoHomes[-1][0])) | bool(re.search(r'([Ee]xam|[Aa]ssignment|[Pp]roblem)', data))):
                self.problemHomes.append((data, self.videoHomes[-1][0]))
                del self.videoHomes[-1]
            elif(bool(re.search(r'lecture[-_]note', self.videoHomes[-1][0])) | bool(re.search(r'[Ll]ecture[\s-][Nn]ote', data))):
                self.lectureNoteHomes.append((data, self.videoHomes[-1][0]))
                del self.videoHomes[-1]
            else:
                del self.videoHomes[-1]

    

class PageParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.handleMode = None
        self.downloadList = list()

    def handle_starttag(self, startTag, attrs):
        if(isListNotNull(attrs) & (startTag == 'a')):
            i = 0
            for res in map(lambda j: j[0]=='href', attrs):
                if(res & isListNotNull(attrs[i])):
                    if(re.search(r'\.mp4$', attrs[i][1])):
                        self.downloadList.append(attrs[i][1])
                    elif(re.search(r'\.pdf$', attrs[i][1])):
                        self.downloadList.append(attrs[i][1])
                i += 1 



if __name__ == "__main__":
    print("Course Name?")
    courseName = input()
    coursePage = coursePage = urllib2.urlopen("https://ocw.mit.edu/courses/"+courseName)
    parser = CourseParser()
    parser.feed(str(coursePage.read().decode("UTF-8")))
    
    print("\nCourse Number?")
    classNum = input()
    i = 0
    homePageList = list(tuple())
    for res in parser.searchCourseNum(classNum):
        print("\n\t", i+1, ". ", parser.courseList[res][2])
        courseHomePage = courseHomePage = urllib2.urlopen("https://ocw.mit.edu"+parser.courseList[parser.searchCourseNum(classNum)[i]][0])
        homeParser = HomepageParser()
        homeParser.feed(str(courseHomePage.read().decode("UTF-8")))
        print("\t\tVideos")
    
        homePageList.append((homeParser.videoHomes, homeParser.problemHomes, homeParser.lectureNoteHomes))

        for videos in homeParser.videoHomes:
            print("\t\t\t", videos[0], "("+videos[1]+")")
            if(videos[0] != homeParser.videoHomes[-1][0]):
                print(", ")
        print("\n\t\tProblems")
        for probs in homeParser.problemHomes:
            print("\t\t\t", probs[0], "("+probs[1]+")")
            if(probs[0] != homeParser.problemHomes[-1][0]):
                print(", ")
        print("\n\t\tLecture Notes")
        for lecnotes in homeParser.lectureNoteHomes:
            print("\t\t\t", lecnotes[0], "("+lecnotes[1]+")")
            if(lecnotes[0] != homeParser.lectureNoteHomes[-1][0]):
                print(", ")
        
        i += 1

    print("\n\nSelect One.")
    lecNum = input()
    print("Which content do you want?(v/p/l)")
    match input():
        case 'v':
            cont = 0
        case 'p':
            cont = 1
        case 'l':
            cont = 2
    print("Which one?")
    contNum = input()
    pageParser = PageParser()
    print(homePageList[int(lecNum)-1][int(cont)])
    desiredPage = desiredPage = urllib2.urlopen("https://ocw.mit.edu"+homePageList[int(lecNum)-1][int(cont)][int(contNum)-1][1])
    pageParser.feed(str(desiredPage.read().decode("UTF-8")))

    print("\n", pageParser.downloadList)
    print(len(pageParser.downloadList))


    

