from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
  page = """<html>
            <head></head>
            <body>
            <div>
              <div>
              <p>PyPi package info search</p>
              </div>
              <div>
                <form action="result" method="POST">
                  <p>Input keywords to search:</p>
                  <input type="text" id='keywords'></input> <br />
                  <input type="submit" value="Search" />
                </form>
              </div>
              <div>
              <p>You know, for Search!</p>
              </div>
            </div>
            </body>
            </html>"""
  return HttpResponse(page)

def result(request):
  return HttpResponse("Result will be here.")
