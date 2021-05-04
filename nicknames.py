import math
names={'109': ['Karp'], '14': ['Reaper', 'Reapa&#039;', 'Reapa\''], '3': ['RandomizeR'], '9': ['Ben', 'LaserWolf', 'ChatBot'], '12': ['Dietcar', 'Dieter', 'Dietrich'], '1': ['Mystic', 'michael'], '52': ['guy', 'guywithhat', 'snoop.gov', 'Guy', 'lemonnuts', 'angellord01', 'gmite', 'mystic the batman', 'batman', 'coolalien56', 'penut', 'GuyWithShark', 'GestorbenWithShark', 'matt miller', 'birfday guy'], '10': ['Kenigmatic', 'Enig.matic'], '8': ['Aponda'], '19': ['Waffles'], '20': ['Phil', 'HandBanana', 'Everyone'], '13': ['AzraelJaffar', 'Azrael', 'Az Real', 'AJ', 'AzraelPariah'], '22': ['LiquidAngel', 'ReplicaMan35'], '17': ['Lymric'], '23': ['That_Kid'], '25': ['Haplo'], '26': ['Kobu'], '21': ['Red'], '5': ['Cole', 'Dr. Death', 'PboFlow', 'TRIwofl'], '39': ['Dr. Agon', 'gregor'], '41': ['Diage'], '49': ['Iron', 'Ion'], '43': ['Daron'], '18': ['SwoopDoggyDog', 'staticworth', 'swoop'], '46': ['DMGunner'], '56': ['capt_dan'], '65': ['schlingy'], '57': ['euphoria'], '37': ['Conrad', 'KillaCondor', 'conner'], '70': ['TriviaBot'], '86': ['Ribos'], '85': ['eep', 'epplant', 'eggeepjeepwhatislegplant'], '94': ['Trientalis', 'Trent'], '114': ['Death Butt', 'paraffin', 'death butt', 'dead butt', 'death nutt', 'Methphukbuttdeth', 'desu', 'db', 'buttbutt'], '117': ['Cameroni&Cheese', 'Cameroni&amp;Cheese', 'AngryNarwhal', 'Angynawhaaa', 'nawa', 'narwhal', 'Orangeangrygangbanger'], '118': ['Modi Thorson', 'Modi Thursday', 'Mightyhightymodilowti', 'Moði Thorson'], '122': ['anime'], '124': ['Valex'], '120': ['ktern'], '189': ['bigbird'], '199': ['vorporeal'], '203': ['liftedpixel'], '208': ['Rocuronium', 'adderallforall', 'Levetiracetam', 'pills', 'rocu'], '206': ['yeagz'], '201': ['xazarus'], '32': ['zoomlaski6', 'zoom'], '215': ['xazBot'], '216': ['Lord Monochromicorn']}
name_lookup = {}
name_list = []
failed = []

for profile in names.keys():
    for name in names[profile]:
        if name in name_lookup.keys():
            print(name, names[profile])
        name_lookup[name] = profile
        name_list.append(name)

def name_find(nick):
    nick = nick.lower()
    candidates=[]
    if nick in name_lookup.keys():
        return names[name_lookup[nick]][0]
    for n in name_list:
        if nick in n.lower() or n.lower() in nick:
            candidates.append(n)
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) > 1:
        new_candidates = list(filter(lambda x: x.lower().find(nick)==0,candidates)) #best bet is that the nick is at the beginning, to avoid coincidences
        if len(new_candidates) != 0:
            candidates = sorted(new_candidates, key=len) #if two match, assume it's the shorter one because the nick matches more of their name
    if len(candidates)==0:
        candidates = name_list
    #l_scores = list(map(lambda x: best_substring_l_distance(nick, x.lower()), name_list)) #find adjusted Levenshtein distances, so we can take the minimum
    #min_score = min(l_scores, key=lambda x: x[0])[0]
    #print(l_scores)
    #print(min_score)
    #max_secondary = -1 #initialized to an impossible value so we know to calculate
    #for i in range(len(l_scores)):
    #    if l_scores[i][0] == min_score:
    #        if max_secondary == -1:
    #            max_secondary = l_scores[i][1]
    #            best_guess = name_list[i]
    #        else:
    #            if l_scores[i][1] > max_secondary:
    #                max_secondary = l_scores[i][1]
    #                best_guess = name_list[i]
    #
    #print(max(list(map(lambda x: best_substring_l_distance(x.lower(),nick), candidates))))
    best_guess = max(candidates, key=lambda x: best_substring_l_distance(x.lower(),nick))
    if best_substring_l_distance(best_guess.lower(), nick) > 1.75: #based on my tests, this is a decent benchmark
        return(best_guess)
    elif best_substring_l_distance(best_guess.lower(), nick) >= 1.4:
        failed.append((nick, best_guess))
        print((nick, best_guess))
        return(best_guess+"?")
    else:
        return("?")
    #if l_distance(nick, best_guess) > max(len(nick),len(best_guess))*.65:
    #    return(best_guess+", but idk")
    #else:
    #    return(best_guess)#(name_list[l_scores.index(min(l_scores))]) #find the min, then get their actual name and return it

def l_distance(a, b): #Levenshtein distance of two strings
    archive = []
    for i in range(len(a)+1): #if there's 0 letters of the other, that's i deletions
        archive.append([i])
        archive[i] += [0]*len(b) #fill in the rest with 0's for now, so we don't get index errors
    for j in range(len(b)+1):
        archive[0][j] = j # if there's 0 letters of the other, that's j insertions
    for j in range(1,len(b)+1):
        for i in range(1,len(a)+1):
            if a[i-1] == b[j-1]:
                sub_cost = 0
            else:
                sub_cost = 1
            archive[i][j] = min(archive[i-1][j]+1,          #deletion
                               archive[i][j-1]+1,           #insertion
                               archive[i-1][j-1]+sub_cost)  #substitution, if necessary
    return(archive[-1][-1])

#Levenshtein distance isn't accurately capturing that nicknames are typically very close to
#substrings of one another e.g. 'Benji' for 'Benjamin' one direction or 'Jimothy for 'Jim'
#in the goofier direction

#So let's find the substrings with the smallest possible Levenshtein distance ('Benj','Jim')
#(technically not the best one, but we're avoiding most local minima)
#ideally we want the one with fewer letters removed, i.e. 'Lord A' is a better match for
#'Lord A(zrael)' than 'Lord (Boreal)'

def best_substring_l_distance(a,b,score=-1, removed=0, shortest_word = -1): #initialized some to impossible amounts so we know to calculate them
    if score == -1:
        score = l_distance(a, b)
    if shortest_word == -1:
        shortest_word = min(len(a), len(b))
    #if max(len(a),len(b)) <= 3: #if you have to go this far, is there even any meaning left?
    #    return min(len(a),len(b))**2/shortest_word/((score+1)**2)
    if l_distance(a,b[:-1]) < score or l_distance(a,b[:-2]) < score: #checking whether the next one improves it skips past most false local minima
        if l_distance(a,b[:-1]) < score:
            score -= 1 #no point calculating it again or storing it, changing one letter can only change the score by 1
        return(best_substring_l_distance(a, b[:-1],score,removed+1,shortest_word))
    elif l_distance(a[:-1],b) < score or l_distance(a[:-2],b) < score:
        if l_distance(a[:-1],b) < score:
            score -= 1
        return(best_substring_l_distance(a[:-1], b,score,removed+1,shortest_word))
    elif l_distance(a,b[1:]) < score or l_distance(a,b[2:]) < score:
        if l_distance(a,b[1:]) < score:
            score -= 1
        return(best_substring_l_distance(a, b[1:],score,removed+1,shortest_word))
    elif l_distance(a[1:],b) < score or l_distance(a[2:],b) < score:
        if l_distance(a[1:],b) < score:
            score -= 1
        return(best_substring_l_distance(a[1:], b,score,removed+1,shortest_word))
    else:
        #print(a,b)
        return min(len(a),len(b))/(score+1) - removed/10 #want lots of letters left with a low score, and not too many removed; took a bit of trial and error to get right
