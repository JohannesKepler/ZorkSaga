from Tkinter import *
import ZorkLore
from os.path import exists
#import json

print "You've awoken in a dark and scary cave.\nYou can't quite remember how you got here, but you know that you were living in a small village on the edge of a forest.\nYou appear unharmed, and you cannot hear any immediate threats.\nBut you know that you won't stay safe for long.\nYou need to find something to defend yourself with, and get out of here!\n"
print "You have a few options at your disposal in this quest.\n"
print "You can remember some things from your past with the word remember."
print "You can inspect something closer with the letter x (for examine)."
print "You can move around with the word go."
print "You can acquire items with the word take."
print "You can check where you are or what you have with the word check."
print "You can see which way you can go with the word look.\n"
print "It's time to start your adventure! See if you can make it out of the cave alive, with your sanity intact!\n"
print "What would you like to do first?\n"

#on save, check for minimap.txt file. If exists, overwrite (with dungeon array). If not, create and write to. on quit, delete file.

#global variables: pos (current position), items (current items), corridor (static map grid), spidey/snakey ('1' or '0' indicating boss status)
with open("ZorkPos.txt", 'r') as xy:
    pos = [line.strip() for line in xy]
    pos = map(int, pos)

with open("ZorkInv.txt", 'r') as inv:
    items = [line.strip() for line in inv]

corridor = []
with open("ZorkGrid.txt", 'r') as grid:
    for line in grid:
        corridor.append(line.split())
        
bosstxt = []
with open("ZorkBoss.txt", 'r') as boss:
    for line in boss:
        bosstxt.append(line.split())
for i in bosstxt:
    if i[0] == 'spider:':
        spidey = i[1]
    elif i[0] == 'snake:':
        snakey = i[1]
    else:
        pass

#get size of map grid
a = len(corridor)
b = len(corridor[0])

#create dungeon map initially filled with ?'s
if exists("ZorkMap.txt"):
    dungeon = []
    with open("ZorkMap.txt", 'r') as minimap:
        for line in minimap:
            dungeon.append(line.split())
    print "Imported saved map file."
else:
    dungeon = [['?' for i in xrange(b)] for j in xrange(a)]
    #starting (home) position
    dungeon[4][2] = "1"
    print "Created new, blank map."

hintful = 0

window = Tk()
#window2 = Tk()
display_grid = Text(window)
display_grid.pack()
#known_map = Text(window2)
#known_map.pack()
window.geometry('260x150+500+100')
window.title('Minimap')
#window2.geometry('260x150+500+100')
#window2.title('Known map')

def hint():
    global hintful
    hints = ['Try examining the cave!', 'Try remembering yourself!', 'Better find a torch in this dark cave!']
    print hints[hintful] + '\n'
    hintful += 1
    if hintful == 3:
        hintful = 0
        
def help():
    helpful = ["List of commands:",
    "go: moves you around. 'go north' or 'move north' are acceptable.",
    "look: see where you can go. you are in a x-, y-coord grid, and move within that plane.",
    "x: examine something - type a word after x for something specific, or just x for a list of what is around you.",
    "take: pick something up if it is near you",
    "remember: remember something that may be useful. history of the place you're in or your own strengths/weaknesses.",
    "i: check the items you are holding (inv)."
    "map: be amazed by my programming prowess and\nsee as much of the map as you have been or seen"]
        
def look():
    global dungeon
    print "It looks like you can go..."
    wall = False
    walkway = True
    if pos == [2, 4]:
        print "Home! Go north!\n"
    else:
        #check north; try-catch error if looking off the map
        pos[1] += 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
        finally:
            if wall == False and walkway == True:
                print "North"
                dungeon[(4-pos[1])][(2+pos[0])] = "0"
            else:
                pass
        #check south
        pos[1] -= 2
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
        finally:
            if wall == False and walkway == True:
                print "South"
                dungeon[(4-pos[1])][(2+pos[0])] = "0"
            else:
                pass
        #check east
        pos[1] += 1
        pos[0] += 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
        finally:
            if wall == False and walkway == True:
                print "East"
                dungeon[(4-pos[1])][(2+pos[0])] = "0"
            else:
                pass
        #check west
        pos[0] -= 2
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
        finally:
            if wall == False and walkway == True:
                print "West"
                dungeon[(4-pos[1])][(2+pos[0])] = "0"
            else:
                pass
        pos[0] += 1
        print '\n'

#the remember command. looks at the string after the word 'remember' and tries to pick out keywords. I would like to have ZorkLore hold all the text (intro, memories, examines) so that it doesn't take up as much space in the main program.

def remember(memory):
    if "village" in memory:
        print "Your village was named Tuusuka.\n"
    elif "myself" in memory:
        print "You are a strong warrior, though sometimes clumsy. You think that must be how you have\ncome to be in this dark and scary cave. You recall a time that you hit\nyour head on a LOW HANGING BEAM as you tried to find your way through your simple house ONE NIGHT.\nYou recall another time you embarrassed yourself when you thought you HEARD\nsomeone call your name, only to wind up interrupting TWO LOVERS trying to share a moment of privacy.\nDespite these shameful times, you remember a time when your sense of SMELL led you and your small troop\nOUT OF THE WOODS that you had been lost in for a week.\nYou SMELLED the smells of a nearby village, whose inhabitants were kind enough to give you shelter and food."
    else:
        print "You can't remember much about that.\n"

#write a command to examine objects.
def examine(ex):
    if "cave" in ex:
        print "The cave is dark and scary.\nYou can hear what might be a rushing stream to the northwest.\nYou can smell something akin to fresh air coming from the northeast.\nAnd you can see what looks like daylight to the south."
    elif ex == "south" or ex == "north" or ex == "east" or ex == "west":
        look()
    elif "spider" in ex and pos == [1, 2] and spidey == '1':
        print "A hideous spider looms before you! It's multi-faceted eyes gleam in the dim light of the cave.\nSuch huge eyes... they look like they don't often see much light..."
    elif "spider" in ex and spidey == '0':
        print "It doesn't look like the spider is going to come back.\n"
    elif "snake" in ex and snakey == '1':
        print "Hopefully you won't find one of those around here...\n"
    elif "snake" in ex and not snakey == '1':
        print "You sure showed that snake.\n"
    else:
        print "I don't know what that is.\n"

#write a command to take objects. stored in ZorkInv.txt
def take(inv):
    global pos
    global items
    if "rock" in inv and pos == [0, 1] and not "rock" in items:
        print "You have a rock now.\n"
        items.append(inv)
    elif "torch" in inv and pos == [-1, 1] and not "torch" in items:
        print "You have a torch now.\n"
        items.append(inv)
    elif "sword" in inv and pos == [0, 2] and not "sword" in items:
        print "You have a sword now.\n"
        items.append(inv)
    elif "cave troll" in inv and not "cave troll" in items:
        print "You have a cave troll.\n"
        items.append(inv)
    else:
        print "I don't see that here.\n"

#write a command to navigate the world. position stored in ZorkPos.txt upon save()
def move(loc):
    global pos
    global dungeon
    global spidey
    global snakey
    wall = False
    walkway = True
    #check matrix of game map to let move function know if a move is legal or not
    if "north" in loc:
        pos[1] += 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
            pos[1] -= 1
        finally:
            if wall == False and walkway == True:
                print "You walk north.\n"
                dungeon[(4-pos[1])][(2+pos[0])] = "1"
                dungeon[(5-pos[1])][(2+pos[0])] = "0"
            elif wall == False and walkway == False:
                print "There's a wall there.\n"
            else:
                print "Invisible walls!\n"
    elif "south" in loc:
        pos[1] -= 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
            pos[1] += 1
        finally:
            if wall == False and walkway == True:
                print "You walk south.\n"
                dungeon[(4-pos[1])][(2+pos[0])] = "1"
                dungeon[(3-pos[1])][(2+pos[0])] = "0"
            elif wall == False and walkway == False:
                print "There's a wall there.\n"
            else:
                print "Invisible walls!\n"
    elif "east" in loc:
        pos[0] += 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
            pos[0] -= 1
        finally:
            if wall == False and walkway == True:
                print "You walk east.\n"
                dungeon[(4-pos[1])][(2+pos[0])] = "1"
                dungeon[(4-pos[1])][(1+pos[0])] = "0"
            elif wall == False and walkway == False:
                print "There's a wall there.\n"
            else:
                print "Invisible walls!\n"
    elif "west" in loc:
        pos[0] -= 1
        try:
            if corridor[(4-pos[1])][(2+pos[0])] == "0":
                walkway = False
            else:
                walkway = True
        except:
            wall = True
            pos[0] += 1
        finally:
            if wall == False and walkway == True:
                print "You walk west.\n"
                dungeon[(4-pos[1])][(2+pos[0])] = "1"
                dungeon[(4-pos[1])][(3+pos[0])] = "0"
            elif wall == False and walkway == False:
                print "There's a wall there.\n"
            else:
                print "Invisible walls!\n"
    elif "home" in loc:
        print "Okay, back where we started.\n"
        pos = [0, 0]
    else:
        print "I don't think you can move there.\n"
    if pos == [-1, 1] and not "torch" in items:
        print "Hey, is that a torch?"
    if pos == [1, 2] and spidey == '1':
        fight("spider", 0)
    elif pos == [2, 4] and snakey == '1':
        fight("snake", 0)
    elif pos == [2, 5] and (spidey == '0' and snakey == '0'):
        print "You escaped the cave! You really are something else.\nYou overcame both the substantial spider and the sinister snake.\nGreat job!\n"
        lose("You win!")
    elif pos == [2, 5] and not (spidey == '0' and snakey == '0'):
        print "You escaped the cave! But you can't help feeling like something evil is watching you go..."
        lose("You win...?")
    else:
        pass
    return pos

#see where you are or what you have
def check(x):
    if "inv" in x:
        for i in items:
            print i
    elif "map" in x:
        print pos
    else:
        print "See inventory (inv) or current position (map)?"
        ask = raw_input('> ')
        check(ask)
        
#display or update automap. called with 1 from move command, called with 2 from look command, called with 3 from check_map command.
def check_map(show_user):
    #global dungeon
    #if show_user == 1:
    #    dungeon[(4-pos[1])][(2+pos[0])] = '1'
    if show_user == 2:
        print "Map"
        for i in dungeon:
            print i
        print "A '1' indicates a corridor - somewhere you have been or looked.\nA '0' indicates a wall - somewhere you have tried to go but been unable.\nAn 'x' indicates somewhere you have not explored - moved or looked."
        print "You awoke at position (5, 3)."
        print "Your position will display this point as [0, 0], ie. the origin."
        print "Your current location is %r" % pos
    else:
        pass
    
#write a couple fight sequences. use a for loop to iterate on chances the player has to examine. for example, they start with 4 moves and if they choose to examine the monster, they are reduced to 3 moves. but the examine will hopefully tell them how to win. if they use the wrong item on the monster - auto-lose?
def fight(atk, i):
    global spidey
    global snakey
    if atk == "spider":
        print "As you round the next corner, your progress is halted by a humongous spider!\nVenom drips from its mandibles, as though salivating at the sight of you!\nYou've probably only got a few seconds before it gets you,\nso you'd better make them count! What do you do?\n"
        k = 3
        print "You've got %d tries!" % (k + 1)
        while i < 4:
            mot = raw_input("> ").lower()
            if mot[0] == "x":
                examine(mot[2:])
                if k > 0:
                    print "You've only got %d turns left!\n" % k
                else:
                    pass
                i += 1
                k -= 1
            elif mot[0:3] == "use":
                if "torch" in mot[4:] and "torch" in items:
                    print "You brandish your torch boldly and drive the evil monster back! Good job!\n"
                    print "Your score goes up by 1.\n"
                    spidey = '0'
                    main()
                elif "torch" in mot[4:] and not "torch" in items:
                    print "You don't have a torch! You'd better find one!\nTry to escape the monster so you can go look!"
                    k = i
                    fight("spider", k)
                else:
                    print "The devil spider overwhelms you with its powerful legs.\nThe last thing you see is the dripping mandibles of the monster\n closing around your head.\n"
                    lose("You lose!")
            elif mot[0:4] == "move" or mot[0:2] == "go":
                if mot[5:] == "south" or mot[3:] == "south":
                    move("south")
                    break
                else:
                    print "Wrong way! The spider catches you and gobbles you up!"
                    lose("You lose!")
            else:
                print "I don't think that will work now!\nTry examining the monster to see if it has a weakness!\n"
                if k > 0:
                    print "You've only got %d turns left!\n" % k
                else:
                    pass
                i += 1
                k -= 1
        print "As you waste time trying to think of what to do,the spider moves with incredible speed\nand snatches you up! You are dragged back to its lair as you slowly lose consciousness.\n"
        lose("You lose!")
    elif atk == 'snake':
        score = 0
        print "With the exit in sight, your spirits rise!\nThe feeling is temporary, however, as your way is suddenly impeded by a hissing snake!\n"
        print "'Ssssso nice to finally meet you, adventurer!' the snake says, laying hard on the S's."
        print "'I've been monitoring your progressss for quite ssssome time,' it continuessss, not making any move toward you yet."
        print "'I'm afraid I cannot let you essscape this cave without anssswering some quessstionsss!'\nAnd with that, the snake emits a horrid, hissing laugh!\n"
        print "You say..."
        first = raw_input("1. You're not so tough!\n2. Please don't hurt me!\n3. Pocket sand!\n> ")
        if first == '1':
            print "'Hissssss! We shall see!'"
        elif first == '2':
            print "'Hissssss! Take courage, human!'"
        elif first == '3':
            print "'Gaaaaaaah!'"
            score += 1
        else:
            print "'Too slow, human!'"
            score -= 1
        print "'First question! At what speed does radio travel?'"
        print "You say..."
        second = raw_input("1. The speed of light!\n2. The speed of fright!\n3. The speed of sound!\n> ")
        if second == '1':
            print "'Gaaaaaaah!'"
            score += 1
        elif second == '2':
            print "'You're not so clever!'"
            score -= 1
        elif second == '3':
            print "'I don't think so!'"
            score -= 1
        else:
            print "'Too slow, human!'"
            score -= 1
        print "'Second question! Do snakes have backbones?'"
        print "You say..."
        third = raw_input("1. Of course! They're vertebrates.\n2. Of course not! They're invertebrates.\n3. HOW DOES SNAKE??\n> ")
        if third == '1':
            print "'Gaaaaaaah!'"
            score += 1
        elif third == '2':
            print "'Who are you calling a coward?'"
            score -= 1
        elif third == '3':
            print "'I don't know, how doesss YOU?'"
            score -= 1
        else:
            print "'Too slow, human!'"
            score -=1
        print "'Final question! Which element accounts for most of the air we breathe?'"
        print "You say..."
        fourth = raw_input("1. Oxygen! (I'm so clever...)\n2. Nitrogen!\n3. My FIST element accounts for most of your FACE! Hya!\n> ")
        if fourth == '1':
            print "'Hahahahahahahaha!'"
            score -= 1
        elif fourth == '2':
            print "'How did you get ssso sssmart?'"
            score += 1
        elif fourth == '3':
            print "'Gaaaaaah!'"
            score += 50
        else:
            print "'Too slow, human!'"
            score -= 1
        if score > 0 and score < 40:
            print "'Well done, human,' the snake sssays. 'You may passssss! But I'll be keeping my eyesss on yousss!'"
            snakey = '2'
        elif score < 0:
            print "'Hahaha! You've failed my tessst! Now I shall eat your mind!' The snake then eats your mind."
            lose("You lose!")
        elif score > 40:
            print "You punched that snake! You are awesome!\nIt went slithering off and you don't think it's going to come back for another taste."
            snakey = '0'
    else:
        pass

#save and quit
def save():
    global pos
    global items
    global bosstxt
    global spidey
    global snakey
    really = raw_input("Save and quit? Y/N ").lower()
    if really == "y":
        print "Come back soon!"
        #write current position back to txt file
        xy = open("ZorkPos.txt", 'w')
        pos = map(str, pos)
        for posit in pos:
            xy.write(posit + '\n')
        xy.close()
        #write current inventory list back to txt file
        yz = open("ZorkInv.txt", 'w')
        yz.write('\n'.join(items))
        yz.close()
        #update bosstxt array with current boss status
        for i in bosstxt:
            if i[0] == 'spider:':
                i[1] = spidey
            elif i[0] == 'snake:':
                i[1] = snakey
            else:
                pass
        #write current boss status back to txt file
        with open("ZorkBoss.txt", 'w') as zz:
            for row in bosstxt:
                zz.write(' '.join(row) + '\n')
        #overwrite minimap file
        with open("ZorkMap.txt", 'w') as xy:
            for row in dungeon:
                xy.write(' '.join(row) + '\n')
        exit(0)
    elif really == "n":
        main()
    else:
        print "Try again, friend.\n"
        save()
        
#loss state: reset text files; exit game without asking to save
def lose(why):
    print why + '\n'
    x = open("ZorkPos.txt", 'w')
    x.write("0\n0")
    y = open("ZorkInv.txt", 'w')
    y.truncate()
    z = open("ZorkBoss.txt", 'w')
    #I need a better way to handle bosses than manually writing and searching and updating this list...
    z.write('spider: 1\nsnake: 1')
    xx = open("ZorkMap.txt", 'w')
    xx.remove()
    x.close()
    y.close()
    z.close()
    exit(0)
    
def quit():
    check = raw_input("Are you sure you want to quit without saving? Y/N ").lower()
    if check == 'y':
        print "Quitting without saving. Thanks for playing!\n"
        exit(0)
    elif check == 'n':
        main()
    else:
        print "Try again, friend.\n"
        quit()    
        
def main():
    #continuous loop to keep the game going. each command calls a function, and when the function concludes the user is automatically returned to the start of main() - unless explicitly stated otherwise
    
    #for i in corridor:
    #    known_map.insert(END, i)

    while True:
        display_grid.delete(1.0, END)
        for i in dungeon:
            display_grid.insert(END, i)

        prompt = '> '
        next = raw_input(prompt).lower()

        if next[0:8] == "remember":
            remember(next[9:])
        elif next[0] == "x":
            examine(next[2:])
        elif next[0:4] == "take":
            take(next[5:])
        elif next[0:2] == "go":
            pos = move(next[3:])
        elif next[0:4] == "move":
            pos = move(next[5:])
        elif next[0:4] == "save":
            save()
        elif next[0:5] == "check":
            check(next[6:])
        elif next[0:4] == "hint":
            hint()
        elif next[0:4] == "help":
            help()
        elif next[0:4] == "look":
            look()
        elif next[0:4] == "quit":
            quit()
        elif next == "whoami" or next == "who am i":
            remember('myself')
        elif next == "whereami" or next == "where am i":
            check('map')
            look()
        elif next[0:3] == "map":
            check_map(2)
        else:
            print "I don't know what that means!\n"

if __name__ == "__main__":
    main()
