from pathlib import Path
PREF_FILE = "musicrecplus.txt"

def loadUsers(fileName):
  '''reads the file containing all the data. If the file doesn't exist, creates a new file. Returns a dictionary of user names and preferred artists-CS'''

  path = Path(fileName)
  if path.is_file() == False:
    with open(fileName, 'w') as f:
      f.write("")
  file = open(fileName, 'r')
  userDict = {}
  for line in file:
    # Read and parse a single line
    [userName, bands] = line.strip().split(":")
    bandList = bands.split(",")
    bandList.sort()
    userDict[userName] = bandList
  return userDict
  file.close()


def showPref(userName, userMap):
  ''' simple show Preferences function for extra credit. Acts as a getPrefs and also can be used to set preferences in the case that a user with no preferences calls the function.
(the function runs on start so a new user can enter their preferences)- MW'''
  if userName in userMap:
    x = []
    for band in userMap[userName]:
      x.append(band)
    return x
  else: 
    prefs = []
    print("I see that you are a new user.")
    print("Please enter the name of an artist or band")
    newPref = input("that you like: ")
    while newPref != "":
      prefs.append(newPref)
      prefs.sort()
      # Always keep the lists in sorted order for ease of comparison
      saveUserPreferences(userName, prefs, userMap, PREF_FILE)
      newPref = input("Enter another band or press enter to continue to main menu: ")
  return prefs

def showMenu(userName, prefs, userMap, PREF_FILE):
  '''This is the opening function within our main and it asks the user what functions it would like the recommender to do and calls upon our helper functions. This also saves our data. - NK'''
  print("\n\nEnter a letter to choose an option:")#give the user the rundown of options
  print(" e - Enter new preferences\n", "s - See current preferences\n",
        "r - Get recommendations\n", "p - Show most popular artists\n",
        "h - How popular is the most popular\n",
        "m - Which user has the most likes\n", "d - Choose preferences to remove\n", "q - Save and quit")
#if statement for the options.
  UserChoice = input()
  if UserChoice == "e":
    prefs = EnterPrefs()
    userMap[userName] = prefs
    print("New preferences loaded")
    showPref(userName, userMap)
  elif UserChoice == "r":
    recs = getRecommendations(userName, prefs, userMap)
    if recs == "Sorry, no users to get recommendations from":
      print("No recommendations available at this time")
    elif len(recs) > 0:
      for t in recs:
        print(t)
    else:
      print("No recommendations available at this times")
  elif UserChoice == "p":
    print(bandMostLikes(userMap)[0])
  elif UserChoice == "m":
    print(userMostLikes(userMap))
  elif UserChoice == "h":
    print(bandMostLikes(userMap)[1])
  elif UserChoice == "s":
    print(userName + "'s preferences are: ", showPref(userName, userMap))
  elif UserChoice == 'd':
    prefs = deletePrefs(userName, userMap)
    userMap[userName] = prefs
  elif UserChoice == "q":
    saveUserPreferences(userName, prefs, userMap, PREF_FILE)
    quit()
  #show the menu again after receiving an input.
  showMenu(userName, prefs, userMap, PREF_FILE)
def userMostLikes(userMap):
  ''' This is a function written by MW, the function takes the userMap that is most up to date and returns either the name of the user with the most liked artists, or no user found if there is no users with any likes.'''
  #working
  max = -1
  most = None
  for user in userMap:
    if user[-1] != '$':
      if len(userMap[user]) > max:
        most = user
        max = len(userMap[user])
  if most == None:
    return "Sorry, no user found."
  return most


def bandMostLikes(userMap):
  '''This is a function written by MW, the function takes the userMap and loops through the list of dictionaries to find out how many likes each band has. It will then create a string of the three most liked bands and the number of likes the most popular band has, and returns both. - CS'''
  #working
  bandLikes = {}
  for user in userMap:
    if user[-1] != '$':
      for band in userMap[user]:
        if band in bandLikes.keys():
          bandLikes[band] += 1
        else:
          bandLikes[band] = 1
  sortlikes = sorted(bandLikes.items(), key=lambda x: x[1], reverse=True)
  sortlikes = dict(sortlikes)
  z = 0
  ret = ""
  top = list(sortlikes.values())[0]
  sortlikes = list(sortlikes.keys())
  while z < (len(sortlikes)) and z < 3:
    #print("RET", ret, sortlikes[z])
    ret += (sortlikes[z]) + "\n"
    z+=1
  return ret, top
def EnterPrefs():
  '''Simple enter preferences function, this function is used to update userMap when called in show menu function. - NK'''
  #working
  prefs = []
  print("Enter an artist that you like ( Enter to finish ):")
  pref = input()
  while pref != "":
    prefs.append(pref.strip().title())
    print("Please enter another artist or band that you")
    print("like, or just press enter")
    pref = input("to see your recommendations: ")
    # Always keep the lists in sorted order for ease of comparison
    prefs.sort()
  return prefs


def getRecommendations(currUser, prefs, userMap):
  ''' Gets recommendations for a user (currUser) based
  on the users in userMap (a dictionary)
  and the user's preferences in pref (a list).
  Returns a list of recommended artists. - CS'''
  if len(userMap) == 1:
    return "Sorry, no users to get recommendations from"
  else:
    bestUser = findBestUser(currUser, prefs, userMap)
    recommendations = drop(prefs, userMap[bestUser])
  return recommendations


def findBestUser(currUser, prefs, userMap):
  ''' Find the user whose tastes are closest to the current
  user. Return the best user's name (a string) - NK'''
  users = userMap.keys()
  bestUser = None  
  bestScore = -1
  for user in users:
    tt = True
    for y in userMap[user]:
      if y not in prefs:
        tt = False
    if user[-1] != '$' and userMap[currUser] != userMap[user] and tt == False:
      score = numMatches(prefs, userMap[user])
      if score > bestScore and currUser != user:  #and prefs != userMap[user]:  #(neel) I added last and because there should be at least one new artist to recommend so the lists shouldn't be the exact same
        bestScore = score
        bestUser = user
  return bestUser


def deletePrefs(userName, userMap):
  '''Removes elements from preferences.- MW'''
  prefs = showPref(userName, userMap)
  print("Current preferences are:\n", prefs)
  print("Select an artist to remove from your preferences")
  rem = input()
  if rem not in prefs:
    print("artist is not in preferences")
    deletePrefs(userName, userMap)
  else:
    prefs.remove(rem)
  return prefs

def drop(list1, list2):
  ''' Return a new list that contains only the elements in list2 that were NOT in list1. uses a for loop and not in operators. - NK'''
  list3 = []
  for i in list2:
    if i not in list1:
      list3.append(i)
  return list3
def numMatches(list1, list2):
  ''' return the number of elements that match between two sorted lists. Useful for finding most closely related user. - CS'''
  matches = 0
  i = 0
  j = 0
  while i < len(list1) and j < len(list2):
    if list1[i] == list2[j]:
      matches += 1
      i += 1
      j += 1
    elif list1[i] < list2[j]:
      i += 1
    else:
      j += 1
  return matches


def saveUserPreferences(userName, prefs, userMap, fileName):
  ''' Writes all of the user preferences to the file.
  Returns nothing. - CS '''
  userMap[userName] = prefs
  file = open(fileName, "w")
  for user in userMap:
    toSave = str(user) + ":" + ",".join(userMap[user]) + \
    "\n"
    file.write(toSave)
  file.close()
def main():
  ''' The driver function, here we initialize userMap and welcome the user, we show them their current preferences, then show them the main menu where they are able to choose the function they want the music recommender to complete - NK'''
  userMap = loadUsers(PREF_FILE)
  print("Welcome to the music recommender system!")
  userName = input(
    "Please enter your name:\n(include a $ after name to be in private mode)\n"
  )
  print("Welcome,", userName)
  prefs = showPref(userName, userMap)
  print("Your current music preferences include:\n", prefs)
  showMenu(userName, prefs, userMap, PREF_FILE)

if __name__ == "__main__": main()
