import ZorkLore
#import json

print "You've awoken in a dark and scary cave.\nYou can't quite remember how you got here, but you know that you were living in a small village on the edge of a forest.\nYou appear unharmed, and you cannot hear any immediate threats.\nBut you know that you won't stay safe for long.\nYou need to find something to defend yourself with, and get out of here!\n"
print "You have a few options at your disposal in this quest.\n"
print "You can remember some things from your past with the word remember."
print "You can inspect something closer with the letter x (for examine)."
print "You can move around with the word go."
print "You can acquire items with the word take.\n"
print "It's time to start your adventure! See if you can make it out of the cave alive, with your sanity intact!\n"
print "What would you like to do first?\n"

#at the moment I am "saving" the game on every action. I should set up temporal variables that hold position and inventory and only get saved back to text file on the save() command. exit() command would quit without saving. this might speed things up as I should not have to open the txt files every single time the move() command is called.

#global variables: pos (current position), items (current items), corridor (static map grid), spidey/snakey ('1' or '0' indicating boss status)
with open("ZorkMap.txt", 'r') as xy:
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
        #if line.startswith("spider"):
        bosstxt.append(line.split())
for i in bosstxt:
    if i[0] == 'spider:':
        spidey = i[1]
    elif i[0] == 'snake:':
        snakey = i[1]
    else:
        pass

#the remember command. looks at the string after the word 'remember' and tries to pick out keywords.
def remember(memory):
    if "village" in memory:
        print "Your village was named Tusaka.\n"
    else:
        print "You can't remember much about that.\n"

#write a command to examine objects.
def examine(ex):
    if "cave" in ex:
        print "The cave is dark and scary.\n"
    else:
        print "I don't know what that is.\n"

#write a command to take objects. stored in ZorkInv.txt
def take(inv):
    global pos
    global items
    if "rock" in inv and pos == [0, 1]:
        print "You have a rock now.\n"
        items.append(inv)
    elif "torch" in inv and pos == [-1, 0]:
        print "You have a torch now.\n"
        items.append(inv)
    elif "sword" in inv and pos == [0, 2]:
        print "You have a sword now.\n"
        items.append(inv)
    elif "cave troll" in inv:
        print "You have a cave troll.\n"
        items.append(inv)
    else:
        print "I don't see that here.\n"

#write a command to navigate the world. position stored in ZorkMap.txt
def move(loc):
    global pos
    global corridor
    global spidey
    global snakey
    #check matrix of game map to let move function know if a move is legal or not
    if "north" in loc:
        pos[1] += 1
        if corridor[(4-pos[1])][(2+pos[0])] == "1":
            print "You walk north.\n"
        else:
            print corridor[(4-pos[1])][(2+pos[0])]
            print "You can't go that way."
            pos[1] -= 1
    elif "south" in loc:
        pos[1] -= 1
        if corridor[(4-pos[1])][(2+pos[0])] == "1":
            print "You walk south.\n"
        else:
            print "You can't go that way."
            pos[1] += 1
    elif "east" in loc:
        pos[0] += 1
        if corridor[(4-pos[1])][(2+pos[0])] == "1":
            print "You walk east.\n"
        else:
            print "You can't go that way."
            pos[0] -= 1
    elif "west" in loc:
        pos[0] -= 1
        if corridor[(4-pos[1])][(2+pos[0])] == "1":
            print "You walk west.\n"
        else:
            print "You can't go that way."
            pos[0] += 1
    elif "home" in loc:
        print "Okay, back where we started.\n"
        pos = [0, 0]
    else:
        print "I don't think you can move there.\n"
    if pos == [1, 2] and spidey == '1':
        fight("spider", 0)
    elif pos == [2, 4] and snakey == '1':
        fight("snake", 0)
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

#write a couple fight sequences. use a for loop to iterate on chances the player has to examine. for example, they start with 4 moves and if they choose to examine the monster, they are reduced to 3 moves. but the examine will hopefully tell them how to win. if they use the wrong item on the monster - auto-lose?
def fight(atk, i):
    global spidey
    global snakey
    if atk == "spider":
        print "As you round the next corner, your progress is halted by a humongous spider!\nVenom drips from its mandibles, as though salivating at the sight of you!\nYou've probably only got a few seconds before it gets you,\nso you'd better make them count! What do you do?\n"
        k = 3
        print "You've got %d tries!" % (k + 1)
        with open("ZorkInv.txt", 'r') as inv:
            items = [line.strip() for line in inv]
        while i < 4:
            mot = raw_input("> ")
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
                    lose()
            elif mot[0:4] == "move":
                if mot[5:] == "south":
                    move("south")
                else:
                    print "Wrong way! The spider catches you and gobbles you up!"
                    lose()
            else:
                print "I don't think that will work now!\nTry examining the monster to see if it has a weakness!\n"
                if k > 0:
                    print "You've only got %d turns left!\n" % k
                else:
                    pass
                i += 1
                k -= 1
        print "As you waste time trying to think of what to do,the spider moves with incredible speed\nand snatches you up! You are dragged back to its lair as you slowly lose consciousness.\n"
        lose()
    else:
        main()

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
        xy = open("ZorkMap.txt", 'w')
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
        exit(0)
    elif really == "n":
        main()
    else:
        print "Try again, friend.\n"
        save()
        
#loss state: reset text files; exit game without asking to save
def lose():
    print "You lose!"
    x = open("ZorkMap.txt", 'w')
    x.write("0\n0")
    y = open("ZorkInv.txt", 'w')
    y.truncate()
    z = open("ZorkBoss.txt", 'w')
    #I need a better way to handle bosses than manually writing and searching and updating this list...
    z.write('spider: 1\nsnake: 1')
    x.close()
    y.close()
    z.close()
    exit(0)
        
def main():
    #continuous loop to keep the game going. each command calls a function, and when the function concludes the user is automatically returned to the start of main() - unless explicitly stated otherwise
    while True:
        prompt = '> '
        next = raw_input(prompt).lower()

        if next[0:8] == "remember":
            remember(next[9:])
        elif next[0] == "x":
            examine(next[2:])
        elif next[0:4] == "take":
            take(next[5:])
        elif next[0:4] == "move":
            pos = move(next[5:])
        elif next[0:4] == "save":
            save()
        elif next[0:5] == "check":
            check(next[6:])
        else:
            print "I don't know what that means!\n"

if __name__ == "__main__":
    main()
