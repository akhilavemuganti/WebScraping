from bs4 import BeautifulSoup as bs
import requests
import urllib3
import os
import time
import pandas as pd

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium import webdriver


url = "http://fracfocusdata.org/DisclosureSearch/Search.aspx"

request = requests.get(url)

driver = webdriver.Chrome('C:/Users/akhila.vemuganti/Downloads/chromedriver_win32_78/chromedriver.exe')
driver.maximize_window()
driver.get(url)
time.sleep(3)



def selectDropDownItem_byId(id,value):
    try:
        dropDown = Select(driver.find_element_by_id(id))
        dropDown.select_by_visible_text(value)
    except(NoSuchElementException) as e:
        print('No such element found')


#Select State
selectDropDownItem_byId('MainContent_cboStateList','Texas')

time.sleep(3)

#Select County
selectDropDownItem_byId('MainContent_cboCountyList','Caldwell')

#Search Button click
search = driver.find_element_by_name('ctl00$MainContent$btnSearch')
search.click()

time.sleep(5)

webPage = driver.page_source
soup = bs(webPage,'html.parser')

# Search Results Table
table = soup.find('table', attrs={'id':'MainContent_GridView1'})
tbody = table.find('tbody')

theader = tbody.find_all('th') #Find all the column Headings in the table
columnsList = [] #List of table columns
for i in range(1,len(theader)): #Skip the first column header since it is empty(PDF Image Heading)
    for h in theader[i]:
        columnsList.append(h.getText())

api_no = []
jobStartDate = []
jobEndDate = []
state = []
county = []
operator =[]
wellName =[]

trows = tbody.find_all('tr') #Find all the rows data

nextPage = soup.find('tr',attrs={'class':'PagerStyle'})
if(nextPage): #If the NextPage button is displayed,skip first two tr's(0,1) and data starts from tr[2]
    startPosition = 2
    upperLimit = len(trows)-1  #Exclude NextPage button row at the bottom of the table
else:
    startPosition = 1
    upperLimit = len(trows)

for i in range(startPosition,upperLimit): #Loop through all the rows in the table
    td = trows[i].find_all('td')

    pdf_xpath = '//*[@id="MainContent_GridView1"]/tbody/tr[' + str(i+1) + ']/td[1]/input'
    print(pdf_xpath)
    pdfImage = driver.find_element_by_xpath(pdf_xpath)
    pdfImage.click()

    time.sleep(2)

    api_no.append(td[1].getText().strip())
    jobStartDate.append(td[2].getText().strip())
    jobEndDate.append(td[3].getText().strip())
    state.append(td[4].getText().strip())
    county.append(td[5].getText().strip())
    operator.append(td[6].getText().strip())
    wellName.append(td[7].getText().strip())

result = {'API_NO':api_no,'Job Start Date':jobStartDate,'Job End Date':jobEndDate,'State':state,'County':county,'Operator':operator,'WellName':wellName}
print(result)

df = pd.DataFrame(result)
print(df)
