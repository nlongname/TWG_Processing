import codecs
#dict of lists of names by profile id (precalculated)
names = {'14': ['Reaper', 'Reapa&#039;'], '3': ['RandomizeR'], '9': ['Ben', 'LaserWolf', 'ChatBot'], '12': ['Dietcar', 'Dieter', 'Dietrich'], '1': ['Mystic'], '52': ['guy', 'guywithhat', 'snoop.gov', 'Guy', 'lemonnuts', 'angellord01', 'gmite', 'mystic the batman', 'batman', 'coolalien56', 'penut', 'GuyWithShark', 'GestorbenWithShark', 'matt miller', 'birfday guy'], '10': ['Kenigmatic', 'Enig.matic'], '8': ['Aponda'], '19': ['Waffles'], '20': ['Phil', 'HandBanana', 'Everyone'], '13': ['AzraelJaffar', 'Azrael', 'Az Real', 'AJ', 'AzraelPariah'], '22': ['LiquidAngel', 'ReplicaMan35'], '17': ['Lymric'], '23': ['That_Kid'], '25': ['Haplo'], '26': ['Kobu'], '21': ['Red'], '5': ['Cole', 'Dr. Death', 'PboFlow'], '39': ['Dr. Agon'], '41': ['Diage'], '49': ['Iron', 'Ion'], '43': ['Daron'], '18': ['SwoopDoggyDog', 'staticworth'], '46': ['DMGunner'], '56': ['capt_dan'], '65': ['schlingy'], '57': ['euphoria'], '37': ['Conrad', 'KillaCondor'], '70': ['TriviaBot'], '86': ['Ribos'], '85': ['eep', 'epplant', 'eggeepjeepwhatislegplant'], '94': ['Trientalis', 'Trent'], '114': ['Death Butt', 'paraffin', 'death butt', 'dead butt', 'death nutt', 'Methphukbuttdeth'], '117': ['Cameroni&amp;Cheese', 'AngryNarwhal', 'Angynawhaaa', 'Orangeangrygangbanger'], '118': ['Modi Thorson', 'Modi Thursday', 'Mightyhightymodilowti', 'Moði Thorson'], '122': ['anime'], '124': ['Valex'], '120': ['ktern'], '189': ['bigbird'], '199': ['vorporeal'], '203': ['liftedpixel'], '208': ['Rocuronium', 'adderallforall', 'Levetiracetam'], '206': ['yeagz'], '201': ['xazarus'], '32': ['zoomlaski6'], '215': ['xazBot'], '216': ['Lord Monochromicorn']} 
taken = ['no lynch'] #gamebreaking name
post_lookup = [0]*100000
recalculate = True
if recalculate:
    for game in range(50):
        try:
            page=1
            while True:
                file = codecs.open("TWG/"+str(game)+"/"+str(page)+".htm", "r", encoding="utf-8", errors='replace')
                text = file.read()
                i=0
                start=0 #these roll around to set the start and end of each substring i need
                end=0
                while i != -1:
                    #find current names on posts
                    i = text.find("\" title=\"View the profile of", i) #on every post, has their profile id right before and name right after
                    #print(i)
                    start = text.find("u=",i-10,i)+2
                    profile = text[start:i]
                    start = text.find(">",i)+1
                    end = text.find("<", start)
                    name = text[start:end]
                    i = end
                    #print(name)
                    if name != '':
                        if profile in names.keys() and name not in names[profile]:
                            names[profile].append(name)
                        elif profile not in names.keys():
                            names[profile] = [name]
                        taken.append(name)
                        #save the profile id on each post to associate quoted names
                        start = text.find("msg_",i)+len("msg_")
                        end = text.find("_", start)
                        post_id = text[start:end]
                        post_lookup[int(post_id)] = profile
                #find quoted (old) names and add them
                i=0
                i = text.find("Quote from: ",i)
                while i != -1:
                    start = i+len("Quote from: ")
                    end = text.find(" on ", start)
                    if end-start > 25 or end==-1: #adjust for non-standard (edited) quotes, which generally don't have post ids
                        end = text.find("<", start)
                    else:
                        name = text[start:end]
                        #if len(name) > 25:
                        #    print("quoted name:", name, game, page, start, end)

                        start = text.find("#msg",start-30)+len("#msg")
                        if start < end: #should be before the name if it's properly formed
                            end = text.find("\"",start)
                            post_id = text[start:end]
                            profile = post_lookup[int(post_id)]

                            if name not in taken and profile != 0:
                                if profile in names.keys() and name not in names[profile]:
                                    names[profile].append(name)
                                elif profile not in names.keys():
                                    names[profile] = [name]
                            taken.append(name)
                    i = text.find("Quote from: ",end+30)
                page += 1
        except FileNotFoundError:
            next
    print(names)
#{'14': ['Reaper', 'Reapa&#039;'], '3': ['RandomizeR'], '9': ['Ben', 'LaserWolf', 'ChatBot'], '12': ['Dietcar', 'Dieter', 'Dietrich'], '1': ['Mystic'], '52': ['guy', 'guywithhat', 'snoop.gov', 'Guy', 'lemonnuts', 'angellord01', 'gmite', 'mystic the batman', 'batman', 'coolalien56', 'penut', 'GuyWithShark', 'GestorbenWithShark', 'matt miller', 'birfday guy'], '10': ['Kenigmatic', 'Enig.matic'], '8': ['Aponda'], '19': ['Waffles'], '20': ['Phil', 'HandBanana', 'Everyone'], '13': ['AzraelJaffar', 'Azrael', 'Az Real', 'AJ', 'AzraelPariah'], '22': ['LiquidAngel', 'ReplicaMan35'], '17': ['Lymric'], '23': ['That_Kid'], '25': ['Haplo'], '26': ['Kobu'], '21': ['Red'], '5': ['Cole', 'Dr. Death', 'PboFlow'], '39': ['Dr. Agon'], '41': ['Diage'], '49': ['Iron', 'Ion'], '43': ['Daron'], '18': ['SwoopDoggyDog', 'staticworth'], '46': ['DMGunner'], '56': ['capt_dan'], '65': ['schlingy'], '57': ['euphoria'], '37': ['Conrad', 'KillaCondor'], '70': ['TriviaBot'], '86': ['Ribos'], '85': ['eep', 'epplant', 'eggeepjeepwhatislegplant'], '94': ['Trientalis', 'Trent'], '114': ['Death Butt', 'paraffin', 'death butt', 'dead butt', 'death nutt', 'Methphukbuttdeth'], '117': ['Cameroni&amp;Cheese', 'AngryNarwhal', 'Angynawhaaa', 'Orangeangrygangbanger'], '118': ['Modi Thorson', 'Modi Thursday', 'Mightyhightymodilowti', 'Moði Thorson'], '122': ['anime'], '124': ['Valex'], '120': ['ktern'], '189': ['bigbird'], '199': ['vorporeal'], '203': ['liftedpixel'], '208': ['Rocuronium', 'adderallforall', 'Levetiracetam'], '206': ['yeagz'], '201': ['xazarus'], '32': ['zoomlaski6'], '215': ['xazBot'], '216': ['Lord Monochromicorn']}
