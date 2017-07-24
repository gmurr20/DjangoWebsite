from django.shortcuts import render, get_list_or_404

import string
import GeneticKnapsack
from models import Company
from models import Project
from models import Photo
from models import Blog
import os
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.
'''
Get the view of the homepage by retrieving work and project info
'''
def index(request):
    try:
        work = get_list_or_404(Company)
        finalWorkList = []
        for w in work:
            if w.photo:
                path = ''+str(w.photo)
                path = path.split('/')
                path = path[len(path)-1]
                path = "/static/"+path
                w.photoPath = path
            finalWorkList.append((w, int(w.duration)))
        finalWorkList = sorted(finalWorkList, key=lambda x: -x[1])
        work = []
        for w in finalWorkList:
            work.append(w[0])
    except:
        work = []
        finalWorkList = []
    try:
        projects = get_list_or_404(Project)
        for p in projects:
            if p.photo:
                path = '' + str(p.photo)
                path = path.split('/')
                path = path[len(path) - 1]
                path = "/static/" + path
                p.photoPath = path
    except:
        projects = []
    return render(request, 'myApp/index.html', {'AllWork': work, 'AllProjects': projects})

'''
Get the photo gallery
'''
def photos(request):
    try:
        photos = get_list_or_404(Photo)
        count = 1
        for p in photos:
            path = '' + str(p.photo)
            path = path.split('/')
            path = path[len(path) - 1]
            path = "/static/uploadedImages/" + path
            p.photoPath = path
            p.index = count
            count += 1
    except:
        photos = []
    return render(request, 'myApp/photoGallery.html', {'Photos': photos})

# http://stackoverflow.com/questions/11476713/determining-how-many-times-a-substring-occurs-in-a-string-in-python
'''
Counts how many times a substring occurs
'''
def substringOccurence(substring, largeString):
   count = 0
   start = 0
   flag = True
   largeString = largeString.lower()
   substring = substring.lower()
   while flag:
       index = largeString.find(substring, start)
       if index == -1:
           flag = False
       else:
           start = index + 1
           count += 1
   return count

'''
Returns html of the blog searches so you can search the blogs
'''
def blogSearch(request):
     try:
        search = str(request.GET.get('search'))
        blogs = get_list_or_404(Blog)
        returnedBlogs = []
        if len(search.lstrip()) == 0 or search == 'None':
            for blog in blogs:
                path = '' + str(blog.image)
                path = path.split('/')
                path = path[len(path) - 1]
                path = "/static/blogPhotos/" + path
                blog.photoPath = path
                returnedBlogs.append((blog,''))
        else:
            for blog in blogs:
                path = '' + str(blog.image)
                path = path.split('/')
                path = path[len(path) - 1]
                path = "/static/blogPhotos/" + path
                blog.photoPath = path
                #count occurrences
                count = substringOccurence(search, str(blog.title))
                count += substringOccurence(search, str(blog.author))
                count += substringOccurence(search, str(blog.date))
                count += substringOccurence(search, str(blog.description))
                count += substringOccurence(search, str(blog.section1Title))
                count += substringOccurence(search, str(blog.section1Content))
                count += substringOccurence(search, str(blog.section2Title))
                count += substringOccurence(search, str(blog.section2Content))
                count += substringOccurence(search, str(blog.section3Title))
                count += substringOccurence(search, str(blog.section3Content))

                if count > 0:
                    returnedBlogs.append((blog,count))
            returnedBlogs = sorted(returnedBlogs, key=lambda x:-x[1])
            print returnedBlogs
     except:
         blogs = []
         returnedBlogs = []
     results = render(request, 'myApp/blogResults.html', {"blogs": returnedBlogs})
     return results

'''
Gets the blog page results
'''
def blogPage(request):
    blogResults = blogSearch(request)
    blogResults = str(blogResults)[38:]
    return render(request, 'myApp/blogPage.html', {"blogResults": blogResults})

'''
Gets an individual blog article with an id
'''
def blogArticle(request):
    try:
        path = request.path
        path = path.split('/')
        myId = int(path[len(path)-1])
        blog = get_list_or_404(Blog, id=myId)[0]
        path = '' + str(blog.image)
        path = path.split('/')
        path = path[len(path) - 1]
        path = "/static/blogPhotos/" + path
        blog.photoPath = path
    except:
        blog = {}
    return render(request, 'myApp/blogArticle.html', {"blog" : blog})

'''
render the basketball page
'''
def basketball(request):
    return render(request, 'myApp/fantasyPage.html', {})

# http://stackoverflow.com/questions/14000595/graphing-an-equation-with-matplotlib
'''
creates a matplotlib graph and saves it in static files
'''
def generateGraph(team):
    salary_x = []
    points_y = []
    #graph projected points and salaries
    for key in team:
        for player in team[key]:
            salary = player.salary
            projected = player.projected
            salary_x.append(salary)
            points_y.append(projected)
    yourRoster, = plt.plot(salary_x, points_y, 'o', label='your roster')

    #graph base line
    x = np.array(range(0,12000))
    y = eval('(x/1000.0)*4.0+10')
    base, = plt.plot(x,y, label='salary value')

    plt.title('Value vs Projected')
    plt.ylabel('Points')
    plt.xlabel('Salary')
    plt.legend([yourRoster, base], loc='best')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ultimatePath = os.path.join(BASE_DIR, 'myApp/static/graphs/myPlot.png')
    plt.savefig(ultimatePath)

''''
Runs the modified script for making an optimal lineup
'''
def runScript(request):
    team = GeneticKnapsack.runScript()
    total = GeneticKnapsack.getTeamSalary(team)
    points = GeneticKnapsack.teamStrength(team)
    generateGraph(team)
    data = render(request, 'myApp/lineupResults.html', {'team': team, 'salaryTotal': total, 'pointTotal':points})
    return data