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

def getUrl(url):
	return 'https://www.basketball-reference.com'+url

def getCsv(column_list):
	csv_header = ''
	column_list_len = len(column_list)
	for i in range(0,column_list_len):
			if(i==column_list_len-1):
				csv_header += column_list[i]
			else:
				csv_header += column_list[i] +','
	return csv_header+'\n'

def getListContents(lis):
	header_list= []
	it = ''
	for item in lis:
		if(item.text==it):
			continue
		it = item.text
		header_list.append(item.text)
	return header_list

		
def getMvpInfo(mvp_data,header_list_len):
	mvp_data_list = [0]*header_list_len
	j = 0
	td_list = mvp_data.findAll("td")
	voting_data_location=td_list[2].find("a")["href"]
	mvp_voting_url = getUrl(voting_data_location)
	mvp_vote_page = getReq(mvp_voting_url)
	season = mvp_data.find("th").text[5:]
	writeVoteData(mvp_vote_page,season)
	print(mvp_voting_url)
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

def getYear(i,type):
	if(type=='leader'):
		return i+1980
	elif(type=='draft'):
		return i+1970

def getATagText(a_tag):
	beg_index = 0
	end_index = 0
	index = 0
	for i in a_tag:
		if(i=='>'):
			beg_index = index 
		elif(i=='<' and index>0):
			end_index = index
			break
		index+=1
	return a_tag[beg_index+1:end_index]

def writeVoteData(mvp_vote_page,season):
	mvp_voting_file= 'voting_mvp'+season+'.csv'
	mvp_vote_container = mvp_vote_page.find("table")
	header_container= mvp_vote_container.find("thead").findAll("tr")[1].findAll("th")
	mvp_vote_stats_container = mvp_vote_container.find("tbody").findAll("tr")
	header_list = getListContents(header_container)
	mvp_vote_csv_header = getCsv(header_list)
	f = open(mvp_voting_file,'w')
	f.write(mvp_vote_csv_header)
	for k in range(0,len(mvp_vote_stats_container)):
		mvp_vote_stats = mvp_vote_stats_container[k].findAll()
		mvp_vote_stats_csv = getCsv(getListContents(mvp_vote_stats))
		print(mvp_vote_stats_csv)
		f.write(mvp_vote_stats_csv)
	f.close()

def getMvpStats():
	mvp_url = 'https://www.basketball-reference.com/awards/mvp.html'
	mvp_page = getReq(mvp_url)
	mvp_data_container = mvp_page.find("table",{"id":"mvp_NBA"}).find("tbody").findAll("tr")
	header_list = ([item['data-stat'] for item in mvp_data_container[0].find_all('td', attrs={'data-stat' : True})])
	mvp_csv_header='season,'+(getCsv(header_list))
	mvp_file = 'mvp_1.csv'
	f = open(mvp_file,'w')
	f.write(mvp_csv_header)
	header_list_len = len(header_list)
	for i in mvp_data_container:
		mvp_data_list = getMvpInfo(i,header_list_len+1)
		mvp_csv_row = getMvpCsvRow(mvp_data_list)
		f.write(mvp_csv_row)
	f.close()
	
def getLeaders():
	for j in range (0,49):
		leader_file = 'leader_'+str(getYear(j,'draft'))+'.csv'
		print(leader_file)
		f = open(leader_file,'w')
		header = 'Type,Name,Stat-Value\n'
		f.write(header)
		base_leader_url = '/leagues/NBA_' + str(getYear(j,'draft')) + '_leaders.html'
		leader_url = getUrl(base_leader_url)
		leader_page = getReq(leader_url)
		leaders_container= leader_page.findAll("div",{"class":"data_grid_box"})
		for k in range (0,len(leaders_container)):
			leader_list = []
			leader_stats_container = leaders_container[k].find("table",{"class":"columns"})
			leader_info= leader_stats_container.find("tr",{"class":"first_place"})
			leader_type = leader_stats_container.find("caption").text
			leader_name = leader_info.find("td",{"class":"who"}).a.text
			leader_stat_value = leader_info.find("td",{"class":"value"}).text
			leader_list.append(leader_type)
			leader_list.append(leader_name)
			leader_list.append(leader_stat_value)
			leader_csv = getCsv(leader_list)
			print(leader_csv)
			f.write(leader_csv)
		f.close()

def getLeagueWinners():
	league_winners_file = 'league_winners.csv'
	league_winners_url = 'https://www.basketball-reference.com/leagues'
	league_winners_page = getReq(league_winners_url)
	league_winners_container = league_winners_page.find("table",{"id":"stats"}).findAll("tr")
	league_winners_header_container = league_winners_container[1].findAll("th")
	league_winners_header_list = []
	for i in range(0,len(league_winners_header_container)):
		header_item =league_winners_header_container[i].text
		league_winners_header_list.append(header_item)
		
	league_winners_header_csv = getCsv(league_winners_header_list)
	f = open(league_winners_file,'w')
	f.write(league_winners_header_csv)
	for i in range(2,len(league_winners_container)):
		league_winners_stats = []
		league_winners_team = league_winners_container[i].find("th").a.text 
		league_winners_stats = league_winners_container[i].findAll("td")
		league_winners_list = []
		league_winners_list.append(league_winners_team)
		for j in league_winners_stats:
			if(not j.a is None):
				league_winners_list.append(j.a.text)
			else:
				league_winners_list.append("None")
		league_winners_csv = getCsv(league_winners_list)
		f.write(league_winners_csv)
	f.close()

def getTeamStats():
	#.encode('utf8')
	for i in range (0,39):
		east_file = 'east'+str(getYear(i,'leader'))+'.csv'
		west_file = 'west'+str(getYear(i,'leader'))+'.csv'
		team_stats_url = 'https://www.basketball-reference.com/leagues/NBA_' + str(getYear(i,'leader'))+'.html#all_team-stats-base'
		team_stats_page = getReq(team_stats_url)
		team_stats_east_container = team_stats_page.findAll("table")[0].findAll("tr")
		team_stats_west_container = team_stats_page.findAll("table")[1].findAll("tr")
		print(team_stats_url)
		team_header_list = getListContents(team_stats_east_container[0].findAll("th"))
		team_header_list.pop(4)
		team_header_csv = getCsv(team_header_list)
		#print(team_header_csv)
		e = open(east_file,'w')
		w = open(west_file,'w')
		print(str(getYear(i,'draft')))
		e.write(team_header_csv)
		w.write(team_header_csv)
		index = 0
		for j in team_stats_east_container:
			if(index<1):
				index+=1
				continue
			east_list = []
			team_name_tag = str(j.find("a"))
			team_name = getATagText(team_name_tag)
			east_list.append(team_name)
			m = 0
			for k in j.findAll("td"):
				if(m==3):
					m+=1
					continue
				east_list.append(k.text)
				m+=1
			east_stats_csv = getCsv(east_list)
			print(east_stats_csv)
			e.write(east_stats_csv)

		index = 0
		for j in team_stats_west_container:
			if(index<1):
				index+=1
				continue
			west_list = []
			team_name_tag = str(j.find("a"))
			team_name = getATagText(team_name_tag)
			west_list.append(team_name)
			m = 0
			for k in j.findAll("td"):
				if(m==3):
					m+=1
					continue
				west_list.append(k.text)
				m+=1
			west_stats_csv = getCsv(west_list)
			print(west_stats_csv)
			w.write(west_stats_csv)

def getDraftPick():
	for i in range(0,48):
		draft_file = 'draft'+str(getYear(i,'draft'))+'.csv'
		draft_pick_url = 'https://www.basketball-reference.com/draft/NBA_'+str(getYear(i,'draft'))+'.html'
		#https://www.basketball-reference.com/draft/NBA_1970.html
		draft_page = getReq(draft_pick_url)
		draft_container = draft_page.find("table",{"id":"stats"})
		draft_picks_container = draft_container.find("tbody").findAll("tr")
		#print(len(draft_picks_container))
		#break
		draft_header_list = draft_container.find("thead").findAll("tr")[1].findAll("th")
		draft_header = getListContents(draft_header_list)
		draft_header_csv = getCsv(draft_header)
		print(draft_pick_url)
		f = open(draft_file,'w')
		f.write(draft_header_csv)
		draft_year_index = 0
		for j in draft_picks_container:
			if(draft_year_index==10):
				break
			draft_row_list = []
			row_index = 0
			for k in j.findAll():
				if(row_index ==1 or row_index ==3 or row_index ==5 or row_index ==7):
					row_index+=1
					continue
				draft_row_list.append(k.text)
				row_index+=1
			draft_year_index+=1
			draft_pick_csv = getCsv(draft_row_list)
			print(draft_pick_csv)
			f.write(draft_pick_csv)
def main():
	#getMvpStats()
	#getLeaders()
	#getLeagueWinners()
	getTeamStats()
	#getDraftPick()


main()