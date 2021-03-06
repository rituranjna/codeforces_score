from django.shortcuts import render
from django.http import HttpResponse
import requests
import urllib.request
import json
import datetime
import shelve
# Create your views here.
def score(request,req_time):
    url="http://codeforces.com/api/user.status?handle=rituraj&from=1&count=10000000";
    req = requests.get(url)
    js= req.json();
    dict={}
    #req_time = "2014-12-16";
    total_point = 0;
    
    ans_string = req_time;

    ans_list = [];
    ans_list.append(req_time);

    for sub in reversed(js["result"]):      
       if( (sub["problem"]["contestId"] , sub["problem"]["index"] ) in dict ):
           continue;
       localseconds = sub["creationTimeSeconds"] #+  gives right time       
       curr_time = datetime.datetime.fromtimestamp(localseconds).strftime('%Y-%m-%d');
       if( curr_time != req_time ):
           continue;          
       dict[ (sub["problem"]["contestId"] , sub["problem"]["index"] ) ] = True;  
       curr_point=0;
       if( sub["problem"]["index"] == "A" ):
           curr_point = 1;
       elif( sub["problem"]["index"] == "B"):
           curr_point = 2;
       elif( sub["problem"]["index"] == "C"):
           curr_point = 5;
       elif( sub["problem"]["index"] == "D"):
           curr_point = 10;
       elif( sub["problem"]["index"] == "E"):
           curr_point = 15;    
       total_point = total_point + curr_point;

       curr_string = "__" + str(sub["problem"]["contestId"]) + "_" + str(sub["problem"]["index"]) + "_" + str(curr_point);       
       ans_string = ans_string  + curr_string;
       ans_list.append(curr_string);
       
    ans_string = ans_string + "__" + " total point is " + str(total_point);

    #insert init database
    sh = shelve.open('test_shelf.db',writeback=True);

    if( req_time in sh ):
        ans_list.append("catched");
    else:    
        sh[req_time] = ans_list;
    sh.close();

    return render(request, 'files/score.html', {'ans_list': ans_list});
