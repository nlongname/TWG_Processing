import codecs
import csv
from collect_names import *
#dict of lists of names by profile id (precalculated, plus some domain knowledge)
names = {'14': ['Reaper', 'Reapa&#039;', 'Reapa\''], '3': ['RandomizeR'], '9': ['Ben', 'LaserWolf', 'ChatBot'], '12': ['Dietcar', 'Dieter', 'Dietrich'], '1': ['Mystic'], '52': ['guy', 'guywithhat', 'snoop.gov', 'Guy', 'lemonnuts', 'angellord01', 'gmite', 'mystic the batman', 'batman', 'coolalien56', 'penut', 'GuyWithShark', 'GestorbenWithShark', 'matt miller', 'birfday guy'], '10': ['Kenigmatic', 'Enig.matic'], '8': ['Aponda'], '19': ['Waffles'], '20': ['Phil', 'HandBanana', 'Everyone'], '13': ['AzraelJaffar', 'Azrael', 'Az Real', 'AJ', 'AzraelPariah'], '22': ['LiquidAngel', 'ReplicaMan35'], '17': ['Lymric'], '23': ['That_Kid'], '25': ['Haplo'], '26': ['Kobu'], '21': ['Red'], '5': ['Cole', 'Dr. Death', 'PboFlow', 'triwofl'], '39': ['Dr. Agon'], '41': ['Diage'], '49': ['Iron', 'Ion'], '43': ['Daron'], '18': ['SwoopDoggyDog', 'staticworth'], '46': ['DMGunner'], '56': ['capt_dan'], '65': ['schlingy'], '57': ['euphoria'], '37': ['Conrad', 'KillaCondor'], '70': ['TriviaBot'], '86': ['Ribos'], '85': ['eep', 'epplant', 'eggeepjeepwhatislegplant'], '94': ['Trientalis', 'Trent'], '114': ['Death Butt', 'paraffin', 'death butt', 'dead butt', 'death nutt', 'Methphukbuttdeth'], '117': ['Cameroni&amp;Cheese', 'AngryNarwhal', 'Angynawhaaa', 'Orangeangrygangbanger'], '118': ['Modi Thorson', 'Modi Thursday', 'Mightyhightymodilowti', 'Moði Thorson'], '122': ['anime'], '124': ['Valex'], '120': ['ktern'], '189': ['bigbird'], '199': ['vorporeal'], '203': ['liftedpixel'], '208': ['Rocuronium', 'adderallforall', 'Levetiracetam', 'pills'], '206': ['yeagz'], '201': ['xazarus', 'xaz'], '32': ['zoomlaski6'], '215': ['xazBot'], '216': ['Lord Monochromicorn']} 
post_archive = [0]*100000
recalculate = True

def post_process(raw):
    start = 0
    end = 0
    quote_depth = 0

    start_tag = "<div class=\"quoteheader\">"
    end_tag = "<div class=\"quotefooter\">"

    start = raw.find(start_tag, start)
    quote_depth = 1
    temp = start+len(start_tag)
    #get rid of quotes
    while start != -1:
        quote_end = raw.find(end_tag, temp)
        if quote_end != -1:
            quote_end += len(end_tag)
        new_quote = raw.find(start_tag, temp)
        if new_quote != -1:
            new_quote += len(start_tag)
        if quote_end < new_quote or new_quote == -1:
            quote_depth -= 1
            if quote_depth == 0:
                raw = raw[:start] + raw[quote_end:]
                start = raw.find(start_tag) #indexes shifted because of what we cut out
                temp = start + len(start_tag)
                quote_depth += 1
        else:
            temp = new_quote
            quote_depth += 1
    #strip tags
    while raw.find('<') != -1:
        raw = raw[:raw.find('<')] +' '+ raw[raw.find('>')+1:]
    #fix ascii symbols (needs to be after you strip the tags or else it could break on those)
    start = 0
    end = 0
    start = raw.find('&#')
    while start != -1:
        end = raw.find(';', start)
        try:
            symbol = chr(int(raw[start+2:end]))
            raw = raw[:start] + symbol + raw[end+1:]
        except ValueError:
            next
        finally:
            start = raw.find('&#', start)
    #fix a couple HTML entities too
    raw = raw.replace('&quot;', '\"').replace('&nbsp;', ' ').replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    #if '&' in raw and ';' in raw:
    #    print(raw)
    return raw.strip()
            
        

if recalculate:
    for game in range(50):
        try:
            page=1
            while True:
                #print(game, page)
                file = codecs.open("TWG/"+str(game)+"/"+str(page)+".htm", "r", encoding="utf-8", errors='replace')
                text = file.read()
                start=0 #these roll around to set the start and end of each substring i need
                end=0
                start = text.find("class=\"inner\" id=\"msg_", end)
                while start != -1:
                    start += len("class=\"inner\" id=\"msg_")
                    end = text.find("\"", start)
                    post_id = text[start:end]
                    start = end+2 #closes out the tag, so we're at the start of the actual message
                    end = text.find("<div class=\"moderatorbar\">", start)
                    raw_post = text[start:end]
                    #print(post_id, raw_post)
                    post_text = post_process(raw_post)
                    #print(post_text)
                    profile = post_lookup[int(post_id)]
                    post_archive[int(post_id)] = [post_text, profile, game, page]
                    start = text.find("class=\"inner\" id=\"msg_", end)
                page += 1
        except FileNotFoundError:
            next
with open('post_archive.csv', 'w', newline='', encoding='utf-8') as csvfile:
    postwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='\'', quoting=csv.QUOTE_ALL)
    postwriter.writerow(['post_id', 'post_text',  'profile_id', 'game', 'page'])
    for i in range(int(post_id) + 1):
        if post_archive[i] != 0:
            postwriter.writerow([str(i)] + post_archive[i])
