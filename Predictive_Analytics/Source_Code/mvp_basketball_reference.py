#importing urlopen function
from urllib.request import urlopen as uReq

#importing beautifulsoup library
from bs4 import BeautifulSoup as soup

#dictionary library
from collections import defaultdict

#Beautiful Soup api used to make requests and download contents of a page
def getReq(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    return page_soup

def getMvpVoteUrl(url):
	return 'https://www.basketball-reference.com'+url

def getCsv(column_list):
	mvp_csv_header = 'season,'
	column_list_len = len(column_list)
	for i in range(0,column_list_len):
		
			if(i==column_list_len-1):
				mvp_csv_header += column_list[i]
			else:
				mvp_csv_header += column_list[i] +','
	return mvp_csv_header+'\n'

def writeVoteData(mvp_vote_page,season):
	mvp_voting_file= 'voting_mvp'+season+'.csv'
	mvp_vote_container = mvp_vote_page.findAll("div",{"class":"index"}).find("div",{"class":"table_wrapper table_controls"})#.find("div",{"class":"table_outer_container"})
	print(len(mvp_vote_container))
def getMvpInfo(mvp_data,header_list_len):
	mvp_data_list = [0]*header_list_len
	j = 0
	td_list = mvp_data.findAll("td")
	voting_data_location=td_list[2].find("a")["href"]
	mvp_voting_url = getMvpVoteUrl(voting_data_location)
	mvp_vote_page = getReq(mvp_voting_url)
	season = mvp_data.find("th").text[5:]
	writeVoteData(mvp_vote_page,season)
	for i in mvp_data:
		if(j==0):
			mvp_data_list[0] =season
		else:	
			mvp_data_list[j] = td_list[j-1].text
		j+=1
	return mvp_data_list 

def getMvpCsvRow(mvp_data_list):
	mvp_data_len = len(mvp_data_list)
	j=0
	mvp_csv_row = ''
	for i in mvp_data_list:
		if(j==mvp_data_len-1):
			mvp_csv_row += i +'\n'
		else:
			mvp_csv_row += i+','
		j+=1
	return mvp_csv_row	


mvp_url = 'https://www.basketball-reference.com/awards/mvp.html'

mvp_page = getReq(mvp_url)
mvp_data_container = mvp_page.find("table",{"id":"mvp_NBA"}).find("tbody").findAll("tr")

header_list = ([item['data-stat'] for item in mvp_data_container[0].find_all('td', attrs={'data-stat' : True})])
mvp_csv_header=(getCsv(header_list))
mvp_file = 'mvp_1.csv'
f = open(mvp_file,'w')
f.write(mvp_csv_header)
header_list_len = len(header_list)
for i in mvp_data_container:
	mvp_data_list = getMvpInfo(i,header_list_len+1)
	mvp_csv_row = getMvpCsvRow(mvp_data_list)
	f.write(mvp_csv_row)