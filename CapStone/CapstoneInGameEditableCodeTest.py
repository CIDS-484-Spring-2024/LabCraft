#needed libraries/files
import TextTset
import importlib
#having a dandy of a time generalizing this code to not just my laptop
#see my walk through video to see this code work for right now
import os
#here we have 2 variables
#that we're going to add using th incomplete method in the TextTset file
a = 2
b = 2


#here is where you can replace the path with the correct one
with open("c:/Users/Zach's LapTop/OneDrive/Desktop/GitLabcraft/labcraftZach/CapStone/TextTset.py", 'r+') as f:
    #prints the file line by line in the counsel
    for x in f:
        print(x)
    #then it takes input (hint "return")
    letstry = input()
    #the input is then wrote to the file
    f.write("    "+letstry+" c\n")

try:
        #ok since python is interperted into bitcode and then ran when you start the program
        #you need to dynamically reload the module
        #thats where the importlib library comes into play
        c = TextTset.addem(a, b)
        # Reload the module
        importlib.reload(TextTset)
        # Retry using the reloaded module
        #btw if you don't put return the whole thing breaks
        c = TextTset.addem(a, b)
    
        print(c)
except Exception as e:
        #here if it doesn't reload, or you don't put the right term in 
        #it prints this message
        print(f"Failed to reload the module: {e}")


