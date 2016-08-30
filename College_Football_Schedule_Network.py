import re
import pandas as pd
import time

import functions as fnc



#get homepage
url = 'https://www.espn.com'
home = fnc.get_website(url)

print 'got hp'

#get NCAAF page
ncaa_page = home.find("nav",{"id":"global-nav"}).find("a",
        {"itemprop":"url","href":re.compile("^\/(c|C)ollege.*(F|f)ootball\/")}).attrs['href']        
ncaaf = fnc.get_website(url+ncaa_page)

print 'got ncaa'

#get schedule page
teams_page = ncaaf.find("nav",{"id":"global-nav-secondary"}).div.find("a",{"href":re.compile("teams")}).attrs['href']      
teams = fnc.get_website(teams_page)

print 'got teams page'
home = []
away = []
store = pd.DataFrame()


#links for each team
pattern = re.compile('^(@|vs).*')
rmv = re.compile('(@|[0-9]|(vs)|(\s+)|#|\*|;)*')
for team in teams.findAll("h5"):
    team_name = team.a.text
    print team_name
    team_name = team_name.replace(" ", "")
    print team_name
    sched_link = team.parent.find("a",{"href":re.compile("schedule")}).attrs['href']
    team_site = fnc.get_website(url+sched_link)
    
    #gather opponents
    for t in team_site.findAll('td'):
        m = re.search(pattern,t.text)
        if m != None:
            if t.text[0] == '@':
                print team_name, re.sub(rmv,"",m.group(0))
                home.append(re.sub(rmv,"",m.group(0)))
                away.append(team_name)
            else:
                print re.sub(rmv,"",m.group(0)),team_name
                away.append(re.sub(rmv,"",m.group(0)))
                home.append(team_name)
    time.sleep(3)


store['Home'] = home
store['Away'] = away
