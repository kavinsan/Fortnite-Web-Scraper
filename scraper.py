import time;
from selenium import webdriver;
import sys;
 
def printData(data):
    
    for stats in data:
        
        name = stats.find_element_by_xpath('.//div[@class=\"trn-defstat__name\"]').text.lower()
        name = ''.join(x for x in name.title())
        value= stats.find_element_by_xpath('.//div[@class=\"trn-defstat__value\"]').text
        
        message = name + ": " + value
        print(message)

def extract(data, matches):
    
    matchValue = matches.pop(0)
    matches.reverse()
    
    header = "{"
    footer = "}"
    dataStart = header + "\n    \"data\": \n    [\n";
    
    dataBody = dataStart
    
    for type in data:
        dataBody += "\t{\n"
        
        matchValue = matches.pop()
        dataBody = dataBody + "\t    \"" + "matches" + "\": \"" + matchValue + "\",\n"
        
        
        for stats in type:
            
            name = stats.find_element_by_xpath('.//div[@class=\"trn-defstat__name\"]').text.lower().replace("/","").replace("%","Percent")
            name = name[0] + ''.join(x for x in name.title()).replace(" ", "")[1:]
            value= stats.find_element_by_xpath('.//div[@class=\"trn-defstat__value\"]').text
            
            dataBody = dataBody + "\t    \"" + name + "\": \"" + value + "\",\n"
            
        dataEnd = '\n\t},\n' 
        dataBody = dataBody[:-2] + dataEnd
        
    dataBody = dataBody[:-2] + "\n    ]\n"  + footer
    return dataBody;

def create(data):
    f = open("data.json", "w+") 
    f.write(data)
    
def scrape(url):
    driver = webdriver.Chrome("D:\Python Webscrapper\chrome\chromedriver.exe");
    driver.get(url);
    
    if(driver.find_elements_by_class_name('trn-card--error')):
        return print("User does not exist")
        sys.exit(0)
    
    #Get the number of matches for total, solo, duo, squads
    matchesElement = driver.find_elements_by_class_name("trn-card__header-subline");
        
    keys = ['all','solo','duo','squad']
    matchData = []
    
    for i in range(len(keys)):
        matchData.append(matchesElement[i].text.split()[0])
    

    data = driver.find_elements_by_class_name("trn-defstat");
    
    #overall = data[0:7]; #simple data
    solo = data[7:18]
    duo = data[18:29]
    squad = data[29:]
    
    statsData = [solo,duo,squad]
    data = extract(statsData, matchData)
    time.sleep(3)
    driver.quit();
    create(data)
    
def validate(platform):
    
    if((platform != "pc") | (platform != "xbl") | (platform != "psn")):
        return False;
    else:
        return True;

def arguments():
    try:
        sys.argv[1]
    except:
        print("Error: undefined platform (pc, xbl, psn)")
        return False;
        
    try:
        sys.argv[2]
    except:
        print("Error: undefined username")
        return False;
        
    return True;
    
def main():

    if(not arguments()):
        sys.exit(0);

    platform = sys.argv[1]
    username = sys.argv[2]

    url = "https://fortnitetracker.com/profile/" + platform + "/" + username
    
    try:
        scrape(url)
    except:
        print("error")
        sys.exit(0)
        
    print("done")

main()