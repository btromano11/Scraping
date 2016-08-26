from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
import re
import networkx as nx

#Get Website
def get_website(url):
    try:
        html = urlopen(url)
    except (URLError,HTTPError) as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html,'html.parser')
    except AttributeError as e:
        return None
    return bsObj

#get homepage
url = 'https://www.espn.com'
home = get_website(url)

print 'got homepage'

#get NCAAF page
ncaa_page = home.find("nav",{"id":"global-nav"}).find("a",
        {"itemprop":"url","href":re.compile("^\/(c|C)ollege.*(F|f)ootball\/")}).attrs['href']        
ncaaf = get_website(url+ncaa_page)

print 'got ncaa page'

#get schedule page
sched_page = ncaaf.find("nav",{"id":"global-nav-secondary"}).div.find("a",{"href":re.compile("teams")}).attrs['href']      
teams = get_website(sched_page)

print 'got schedule page'
graph = nx.DiGraph()

#links for each team
i=0
pattern = re.compile('^(@|vs).*')
rmv = re.compile('(@|[0-9]|(vs)|(\s+)|#)*')
for team in teams.findAll("h5"):
    team_name = team.a.text
    sched_link = team.parent.find("a",{"href":re.compile("schedule")}).attrs['href']
    team_site = get_website(url+sched_link)
    
    #gather opponents
    for t in team_site.findAll('td'):
        m = re.search(pattern,t.text)
        if m != None:
            if t.text[0] == '@':
                print team_name, re.sub(rmv,"",m.group(0))
                graph.add_edge(team_name, re.sub(rmv,"",m.group(0)))
            else:
                print re.sub(rmv,"",m.group(0)),team_name
                graph.add_edge(re.sub(rmv,"",m.group(0)),team_name)
    i+=1
    if i == 2:
        break