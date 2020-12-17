from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import SearchForm

def index(request):
#  page = """<html>
#            <head></head>
#            <body>
#            <div>
#              <div>
#              <p>PyPi package info search</p>
#              </div>
#              <div>
#                <form action="result/" method="POST">
#                  <p>Input keywords to search:</p>
#                  <input type="text" id='keywords' name='keywords'></input> <br />
#                  <input type="submit" value="Search" />
#                </form>
#              </div>
#              <div>
#              <p>You know, for Search!</p>
#              </div>
#            </div>
#            </body>
#            </html>"""

  return render(request, 'index.html', {'form': SearchForm()})

def result(request):
  for item in request.POST.items():
    print(item)
  return HttpResponse(f"Result will be here.")
