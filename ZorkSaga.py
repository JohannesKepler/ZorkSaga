import ZorkLore

print "You've awoken in a dark and scary cave.\nYou can't quite remember how you got here, but you know that you were living in a small village on the edge of a forest.\nYou appear unharmed, and you cannot hear any immediate threats.\nBut you know that you won't stay safe for long.\nYou need to find something to defend yourself with, and get out of here!\n"
print "You have a few options at your disposal in this quest.\n"
print "You can remember some things from your past with the word remember."
print "You can inspect something closer with the letter x (for examine)."
print "You can move around with the word go."
print "You can acquire items with the word take.\n"
print "It's time to start your adventure! See if you can make it out of the cave alive, with your sanity intact!\n"
print "What would you like to do first?"

#every command sends you back to the prompt at the end. there might be a better way to do this. the program is closing after the first or second call on prompt.
#def prompt(x):
#    x = raw_input("> ")
#    return x

#the remember command. looks at the string after the word 'remember' and tries to pick out keywords.
def remember(memory):
    if "village" in memory:
        print "Your village was named Tusktown.\n"
        main()
    else:
        print "You can't remember much about that.\n"
        main()

#write a command to examine objects.
def examine(ex):
    if "cave" in ex:
        print "The cave is dark and scary.\n"
        main()
    else:
        print "I don't know what that is.\n"
        main()

#write a command to take objects. create new document - or class? - that stores and remembers your inventory.
def take(inv):
    if "rock" in inv:
        print "You have a rock now.\n"
        item_doc = open("ZorkInv.txt", 'a')
        item_doc.write(inv)
        item_doc.write('\n')
        item_doc.close()
        main()
    else:
        print "I don't see that here.\n"
        main()

#write a command to navigate the world. the game needs to remember where you are.
def move(loc):
    with open("ZorkMap.txt", 'r+') as xy:
        pos = [line.strip() for line in xy]
        pos = map(int, pos)
    if "north" in loc:
        print "You walk north.\n"
        pos[1] += 1
    elif "south" in loc:
        print "You walk south.\n"
        pos[1] -= 1
    elif "east" in loc:
        print "You walk east.\n"
        pos[0] += 1
    elif "west" in loc:
        print "You walk west.\n"
        pos[0] -= 1
    elif "home" in loc:
        print "Okay, back where we started.\n"
        pos[0] = 0
        pos[1] = 0
    else:
        print "I don't think you can move there.\n"
        main()
    xy = open("ZorkMap.txt", 'w')
    pos = map(str, pos)
    for posit in pos:
        xy.write(posit + '\n')
    xy.close()
    main()

#save and quit
def save(s):
    if "save" in s:
        print "Come back soon!"
        exit(0)

def main():
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
            move(next[5:])
        elif next[0:4] == "save":
            save(next)
        else:
            print "I don't know what that means!\n"
            main()

if __name__ == "__main__":
    main()
