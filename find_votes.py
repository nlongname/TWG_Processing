import codecs
from collect_names import *
from nicknames import *
import csv

vote_record = [['voter_id', 'voter_name', 'votee_id', 'votee_name', 'post_id', 'datetime', 'game', 'page']]


vote_tag="<b>" #some votes use <b></b>, others <strong></strong>, for the time being I'm just stitching the two sets of votes together manually
for game in range(50):
    #vote_record.append([])
    gm = ''
    try:
        page=1
        while True:
            file = codecs.open("TWG/"+str(game)+"/"+str(page)+".htm", "r", encoding="utf-8", errors='replace')
            text = file.read()
            #find the date scraped to fix "Today" datetimes
            start = text.find("Show new replies to your posts.") #last thing before the date at the top
            start = text.find("<li>", start)+len("<li>") #besides this tag
            end = text.find(",", start)+1 #so it doesn't find the same comma again
            end = text.find(",", end)+1 #one comma between the day and the year, the second is between the year and the time, which we're going to keep
            date_scraped = text[start:end]
            start=0 #these roll around to set the start and end of each substring i need
            end=0
            #print(game, page)
            if gm == '':
                start = text.find("msg_")+len("msg_")
                end = text.find("_", start)
                gm = post_lookup[int(text[start:end])]
            start = text.find(vote_tag, start)
            while start != -1:
                start += len(vote_tag)
                end = text.find("<", start)
                vote_text = text[start:end].lower()
                while "-&gt;" in vote_text:
                    vote_text = vote_text[vote_text.find("-&gt;")+len("-&gt;"):]
                    #print(vote_text, game, page)
                while "&lt;-" in vote_text:
                    vote_text = vote_text[:vote_text.find("&lt;-")]
                    #print(vote_text, game, page)
                if len(vote_text) > 25:
                    vote_text = vote_text[:25]
                #print(start, end, votee)
                if vote_text not in ['go down', 'go up', str(page)]:
                    votee = name_find(vote_text)
                    if votee[-1] != '?':
                        votee = name_lookup[votee]
                        temp_start = -1
                        offset = 0
                        while temp_start == -1:
                            offset += 100
                            temp_start = text.find("msg_", start-offset,start)
                        #print(game, page, start, temp_start, offset, names[votee][0], vote_text)
                        temp_start += len("msg_")
                        end = text.find("\"",temp_start)
                        post=int(text[temp_start:end])
                        voter_id = post_lookup[post]
                        quote_depth = text[:start].count("quoteheader")-text[:start].count("quotefooter")
                        if quote_depth == 0 and voter_id != gm:
                            temp_start = -1
                            while temp_start == -1:
                                offset += 100
                                temp_start = text.find("&#171;", start-offset, start)
                            temp_start = text.find("</b> ", temp_start)+len("</b> ")
                            end = text.find(" &#187;", temp_start)
                            datetime = text[temp_start:end]
                            if 'Today' in datetime:
                                datetime = date_scraped + datetime[len("<strong>Today</strong> at"):]
                            #print(names[voter_id][0], "for", names[votee][0], datetime)
                            vote_record.append([voter_id, names[voter_id][0], votee, names[votee][0], post, datetime, game, page])
                start = text.find(vote_tag, start)
            page += 1
    except FileNotFoundError:
        print(game, "done")
        
with open('vote_record.csv', 'w', newline='') as csvfile:
    votewriter = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_ALL)
    for i in range(len(vote_record)):
        votewriter.writerow(vote_record[i])
