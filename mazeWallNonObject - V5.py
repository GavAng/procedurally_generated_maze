import random
from collections import Counter

#global variables
#-1 represents inner wall, -2 represents outer wall
wallTypes = (-1,-2)



class Player():

    def __init__(self, roomPos):
        self.position = roomPos

    def hitWall(self, direction):
        directions = ("north","east","south","west")
        print(f"\n\n\nYou hit a wall trying to head {directions[direction]}.")

    def moveRoom(self, newRoomPos):
        self.position = newRoomPos
        print(f"\n\n\nYou entered room {newRoomPos}.")




# Defines a singular room that can be placed in a Maze;
#it stores the information of where the player can travel from this room
class Room():

    def __init__(self, position, neighbours):
        self.position = position #position in maze, starting at 0
        self.neighbours = neighbours
        self.routes = list(neighbours) #make routes array mutable

    def editWall(self, direction, update):
        self.routes[direction] = update

    def visualizeRoom(self, player):

        outputRows = [[],[],[],[],[]]


        #if player is in this room make the room's character "P"
        centralKey = "P" if player.position == self.position else str(self.position + 1)


        #if a wall appears to the north of the room
        if self.routes[0] in wallTypes: 
            outputRows[0].append("C-------C")
        else:
            outputRows[0].append("C       C")

        #if a wall appears to the west of the room
        if self.routes[3] in wallTypes: 
            outputRows[1].append("|")
            outputRows[2].append("|")   
        else:
            outputRows[1].append(" ")
            outputRows[2].append(" ")


        outputRows[1].append("       ")

        if len(centralKey) == 1:
            outputRows[2].append("   " + centralKey + "   ")
        elif len(centralKey) == 2:
            outputRows[2].append("  " + centralKey + "   ")
        elif len(centralKey) == 3:
            outputRows[2].append("  " + centralKey + "  ")
        elif len(centralKey) == 4:
            outputRows[2].append(" " + centralKey + "  ")


        #if a wall appears to the east of the room
        if self.routes[1] in wallTypes: 
            outputRows[1].append("|")
            outputRows[2].append("|")
        else:
            outputRows[1].append(" ")
            outputRows[2].append(" ")

        #if a wall appears to the south of the room
        if self.routes[2] in wallTypes: 
            outputRows[4].append("C-------C")
        else:
            outputRows[4].append("C       C")


        return ["".join(row) for row in outputRows]



# Defines a grid of Rooms that can be rendered and played
class Maze():

    def __init__(self, length, height):

        self.length = length
        self.height = height
        self.area = length * height
        self.structure = self.generateStructure()


    def generateStructure(self):

        structure = []

        for roomPos in range(self.area):
            neighbours = self.calculateNeighbours(roomPos)
            structure.append(Room(roomPos, neighbours))

        return structure


    def calculateNeighbours(self, roomPos):

        neighbours = [-2]*4

        #if room is not on the... 
        
        #...west side of the maze
        if roomPos % self.length != 0: 
            neighbours[3] = roomPos - 1

        #...east side of the maze
        if roomPos % self.length != self.length - 1: 
            neighbours[1] = roomPos + 1

        #... north side of the maze
        if roomPos >= self.length: 
            neighbours[0] = roomPos - self.length

         #... south side of the maze
        if roomPos < self.area - self.length:
            neighbours[2] = roomPos + self.length

        return tuple(neighbours) #make neighbour array immutable
    

    def addWall(self, roomPos, direction):

        targetRoom = self.structure[roomPos]

        #if no wall exists at this direction
        if targetRoom.routes[direction] not in wallTypes:

            targetRoom.editWall(direction, -1) #create initial wall

            #create identical wall in same place on opposite room
            converseRoom = self.structure[targetRoom.neighbours[direction]]
            converseRoom.editWall(directionCorrector(direction + 2), -1)
            

    def removeWall(self, roomPos, direction):

        targetRoom = self.structure[roomPos]

        #if an inner wall exists at this direction
        if targetRoom.routes[direction] == -1: 

            targetRoom.editWall(direction, targetRoom.neighbours[direction]) #revert initial route

            #revert identical route in same place on opposite room
            converseRoom = self.structure[targetRoom.neighbours[direction]]
            converseRoom.editWall(directionCorrector(direction + 2), targetRoom.position)


    # Creates a list of all the spaces in the maze where there are no walls present
    def noWallRoutes(self): 

        noWallCoordinates = []

        for room in self.structure:
            for direction, route in enumerate(room.routes):

                if route not in wallTypes:
                    noWallCoordinates.append([room.position, direction])

        return noWallCoordinates


    def visualizeMaze(self, player):

        print()
        for roomPos in range(0, self.area, self.length):
            
            printLines = [[],[],[],[],[]]
            printLines[3] = printLines[1]


            for currentPos in range(roomPos, roomPos+self.length):

                roomVisualization = self.structure[currentPos].visualizeRoom(player)

                #only display the right side of a room if it is on the east side of the maze
                if currentPos % self.length == self.length - 1:
                    for printLine, roomVisual in zip(printLines, roomVisualization):
                        printLine.append(roomVisual)
                else:
                    for printLine, roomVisual in zip(printLines, roomVisualization):
                        printLine.append(roomVisual[:-1])


            print(*map("".join, printLines[:4]), sep="\n")        
        #only display the bottom side the maze on the last row
        print("".join(printLines[4]))

    

    def startGame(self):

        protagonist = Player(0) #create player in first room
        currentRoom = self.structure[0] #set initial room as first room

        repeatRoom = False


        while True:

            self.visualizeMaze(protagonist)


            if not repeatRoom:
                chosenDirection = input(f"\nYou are in room {protagonist.position}. What direction would you like to move?").lower()

            else: #if you were in the same room in the last loop
                chosenDirection = input(f"\nYou are still in room {protagonist.position}. What direction would you like to move?").lower()

            repeatRoom = False


            if chosenDirection[0] in ["n","u","0"]:
                direction = 0

            elif chosenDirection[0] in ["e","r","1"]:
                direction = 1

            elif chosenDirection[0] in ["s","d","2"]:
                direction = 2

            elif chosenDirection[0] in ["w","l","3"]:
                direction = 3

            else:
                print("\n\n\nNot a valid input.")
                repeatRoom = True
                continue


            potentialRoomPos = currentRoom.routes[direction]


            #if move takes player into a wall
            if potentialRoomPos in wallTypes: 
                protagonist.hitWall(direction)

                repeatRoom = True

            #if move takes player into a new room
            else: 
                protagonist.moveRoom(potentialRoomPos)
                currentRoom = self.structure[potentialRoomPos]



# Calculates the maximum amount of walls you can fit in a maze will still allowing maneuverability
def optimumWallCountFinder(length, height): 
    return (length - 1) * (height - 1)



# Corrects direction if it is outwith the range of 0 to 3 inclusive
def directionCorrector(direction): 
    return direction % 4



# Returns false if a room has 3 walls
def wallCountChecker(room): 
    routeCounts = Counter(room.routes)
    return routeCounts[-2] + routeCounts[-1] != 3



# Makes coordinates for a wall
def wallCoordinatesMaker(room, direction): 

    currentWall = [room.position,direction]
    converseWall = [room.neighbours[direction], directionCorrector(direction + 2)]

    return [currentWall, converseWall]



# Checks the coordinates of one wall pair is not in a set of walls coordinate pairs
def wallCoordinatesVerify(room, direction, otherWalls): 

    wallPair = wallCoordinatesMaker(room, direction)

    #return false if there is any intersection between the lists
    return not any(item in otherWalls for item in wallPair)



# Orchestrates the wallChainFinder function and tell it what wall to check next
def wallChainFinderBranch(maze, currentRoom, direction, pastWalls, presentWalls, futureWalls, outerWallCount): 

    if outerWallCount > 1:
        return outerWallCount


    futureWalls.extend(wallCoordinatesMaker(currentRoom, direction))


    routes = currentRoom.routes
    neighbours = currentRoom.neighbours
    #get the room accross from where the current wall being checked is
    converseRoom = maze.structure[neighbours[direction]] 

    sideDirection1 = directionCorrector(direction - 1)
    sideDirection2 = directionCorrector(direction + 1)


    #if there is an outer wall to the first side of this room
    if neighbours[sideDirection1] == -2: 

        outerWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom2 = maze.structure[neighbours[sideDirection2]] 

        futureWalls.extend(wallCoordinatesMaker(converseRoom, sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(sideRoom2, direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom, sideDirection2))


        #if there is a wall to the second side of the converse room and room not already considered
        if converseRoom.routes[sideDirection2] == -1 and wallCoordinatesVerify(converseRoom, sideDirection2, presentWalls): 
            outerWallCount = wallChainFinder(maze, converseRoom, sideDirection2, pastWalls, futureWalls, [], outerWallCount)

        #if there is a wall inline with the current wall on the room to the second side and room not already considered
        if sideRoom2.routes[direction] == -1 and wallCoordinatesVerify(sideRoom2, direction, presentWalls): 
            outerWallCount = wallChainFinder(maze, sideRoom2, direction, pastWalls, futureWalls, [], outerWallCount)

        if routes[sideDirection2] == -1 and wallCoordinatesVerify(currentRoom, sideDirection2, presentWalls):
            outerWallCount = wallChainFinder(maze, currentRoom, sideDirection2, pastWalls, futureWalls, [], outerWallCount)


    #if there is an outer wall to the second side of this room
    elif neighbours[sideDirection2] == -2: 

        outerWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom1 = maze.structure[neighbours[sideDirection1]] 

        futureWalls.extend(wallCoordinatesMaker(converseRoom, sideDirection1))
        futureWalls.extend(wallCoordinatesMaker(sideRoom1, direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom, sideDirection1))


        #if there is a wall to the first side of the converse room and room not already considered
        if converseRoom.routes[sideDirection1] == -1 and wallCoordinatesVerify(converseRoom, sideDirection1, presentWalls):             
            outerWallCount = wallChainFinder(maze, converseRoom, sideDirection1, pastWalls, futureWalls, [], outerWallCount)

        #if there is a wall inline with the current wall on the room to the first side and room not already considered
        if sideRoom1.routes[direction] == -1 and wallCoordinatesVerify(sideRoom1, direction, presentWalls):            
            outerWallCount = wallChainFinder(maze, sideRoom1, direction, pastWalls, futureWalls, [], outerWallCount)

        if routes[sideDirection1] == -1 and wallCoordinatesVerify(currentRoom,sideDirection1,presentWalls):         
            outerWallCount = wallChainFinder(maze, currentRoom, sideDirection1, pastWalls, futureWalls, [], outerWallCount)


    else:
        #get the rooms on either side of this room
        sideRoom2 = maze.structure[neighbours[sideDirection2]] 
        sideRoom1 = maze.structure[neighbours[sideDirection1]]

        #keeps note of all neighbouring walls of the current wall
        futureWalls.extend(wallCoordinatesMaker(converseRoom, sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(sideRoom2, direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom, sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(converseRoom, sideDirection1))
        futureWalls.extend(wallCoordinatesMaker(sideRoom1, direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom, sideDirection1))

        
        #if there is a wall to the second side of the converse room and room not already considered
        if converseRoom.routes[sideDirection2] == -1 and wallCoordinatesVerify(converseRoom, sideDirection2, presentWalls):        
            outerWallCount = wallChainFinder(maze, converseRoom, sideDirection2, pastWalls, futureWalls, [], outerWallCount)

        #if there is a wall inline with the current wall on the room to the second side and room not already considered
        if sideRoom2.routes[direction] == -1 and wallCoordinatesVerify(sideRoom2, direction, presentWalls):            
            outerWallCount = wallChainFinder(maze, sideRoom2, direction, pastWalls, futureWalls, [], outerWallCount)

        if routes[sideDirection2] == -1 and wallCoordinatesVerify(currentRoom, sideDirection2, presentWalls):       
            outerWallCount = wallChainFinder(maze, currentRoom, sideDirection2, pastWalls, futureWalls, [], outerWallCount)

        #if there is a wall to the first side of the converse room and room not already considered
        if converseRoom.routes[sideDirection1] == -1 and wallCoordinatesVerify(converseRoom, sideDirection1, presentWalls):            
            outerWallCount = wallChainFinder(maze, converseRoom, sideDirection1, pastWalls, futureWalls, [], outerWallCount)

        #if there is a wall inline with the current wall on the room to the first side and room not already considered
        if sideRoom1.routes[direction] == -1 and wallCoordinatesVerify(sideRoom1, direction, presentWalls):            
            outerWallCount = wallChainFinder(maze, sideRoom1, direction, pastWalls, futureWalls, [], outerWallCount)

        if routes[sideDirection1] == -1 and wallCoordinatesVerify(currentRoom, sideDirection1, presentWalls):           
            outerWallCount = wallChainFinder(maze, currentRoom, sideDirection1, pastWalls, futureWalls, [], outerWallCount)


    return outerWallCount





# Checks if a wall would obscure part of the maze by connecting two parts of the outer wall
def wallChainFinder(maze, currentRoom, direction, pastWalls, presentWalls, futureWalls, outerWallCount): 

    if outerWallCount > 1:
        return outerWallCount


    currentWallPair = wallCoordinatesMaker(currentRoom, direction)


    #if current wall has already been checked previously, exit this algorithm
    if currentWallPair[0] in pastWalls:
        return 2
    #else add them to the list of checked walls
    pastWalls.extend(currentWallPair)


    outerWallCount = wallChainFinderBranch(maze, currentRoom, direction, pastWalls, presentWalls, futureWalls, outerWallCount)

    
    return outerWallCount





# Checks if a wall is sandwhiched on both sides by other walls
def wallSandwhichFinder(maze, roomPos, direction): 

    targetRoom = maze.structure[roomPos]

    routes = targetRoom.routes
    neighbours = targetRoom.neighbours
    #get the room accross from where the current wall being checked is
    converseRoom = maze.structure[neighbours[direction]] 

    sandwhichWallCount = 0

    sideDirection1 = directionCorrector(direction - 1)
    sideDirection2 = directionCorrector(direction + 1)


    #if there is an outer wall to the first side of this room
    if neighbours[sideDirection1] == -2: 

        sandwhichWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom2 = maze.structure[neighbours[sideDirection2]] 

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection2] == -1 or sideRoom2.routes[direction] == -1 or routes[sideDirection2] == -1:
            sandwhichWallCount += 1


    #if there is an outer wall to the second side of this room
    elif neighbours[sideDirection2] == -2: 

        sandwhichWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom1 = maze.structure[neighbours[sideDirection1]] 

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection1] == -1 or sideRoom1.routes[direction] == -1 or routes[sideDirection1] == -1: 
            sandwhichWallCount += 1


    else:
        #get the rooms on either side of this room
        sideRoom2 = maze.structure[neighbours[sideDirection2]] 
        sideRoom1 = maze.structure[neighbours[sideDirection1]]

        #if there is a wall beside one end of the wall
        if converseRoom.routes[sideDirection2] == -1 or sideRoom2.routes[direction] == -1 or routes[sideDirection2] == -1:
            sandwhichWallCount += 1

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection1] == -1 or sideRoom1.routes[direction] == -1 or routes[sideDirection1] == -1: 
            sandwhichWallCount += 1


    if sandwhichWallCount == 2:
        return True


    return False





# Prodecurally generates a maze
def mazeRandomizer(): 

    length = random.randint(3,10)
    height = random.randint(3,10)

    protagonist = Player(0)
    randomMaze = Maze(length,height)

    #creates a selection pool of all the spaces in the maze where no walls are present
    possibleWallCoordinates = randomMaze.noWallRoutes() 
    addedWallCoordinates = []
    #finds the max walls you could place in the maze while still allowing room movement
    optimumWallCount = optimumWallCountFinder(length,height) 



    for i in range(optimumWallCount):

        #gets a wall from the selection pool
        randomWallCoordinate = random.choice(possibleWallCoordinates) 
        randomRoomPos = randomWallCoordinate[0]
        randomDirection = randomWallCoordinate[1]
        targetRoom = randomMaze.structure[randomRoomPos]


        #if one of the conditions is not met
        while not mazeRandomizerConditions(randomMaze, targetRoom, randomDirection): 

            #removes the wall and converse wall from the selection pool
            possibleWallCoordinates.remove(randomWallCoordinate) 
            possibleWallCoordinates.remove(wallCoordinatesMaker(targetRoom, randomDirection)[1])

            #gets a new wall from the selection pool
            randomWallCoordinate = random.choice(possibleWallCoordinates) 
            randomRoomPos = randomWallCoordinate[0]
            randomDirection = randomWallCoordinate[1]
            targetRoom = randomMaze.structure[randomRoomPos]

        
        #adds wall to maze if conditions are met
        randomMaze.addWall(randomRoomPos,randomDirection) 

        #creates a log of all the successfully added walls
        addedWallCoordinates.append(randomWallCoordinate) 
        
        #removes the wall and converse wall from the selection pool
        possibleWallCoordinates.remove(randomWallCoordinate)
        possibleWallCoordinates.remove(wallCoordinatesMaker(targetRoom, randomDirection)[1])



    #if optimumWallCount >= 10:
        #randomMaze = mazeRandomWallRemover(randomMaze, int(optimumWallCount / 10),addedWallCoordinates)


    randomMaze.visualizeMaze(protagonist)
    #randomMaze.startGame()



# A set of conditions that an added wall must meet
def mazeRandomizerConditions(maze, targetRoom, direction): 

    #if 3 walls already exist in this room
    if not wallCountChecker(targetRoom): 
        return False

    
    #get the room that will be on the opposite side of the wall
    converseRoom = maze.structure[targetRoom.routes[direction]] 
    if not wallCountChecker(converseRoom): #if 3 walls already exist in converse room
        return False


    #if the added wall will obscure parts of the maze
    outerWallCount = wallChainFinder(maze, targetRoom, direction, [], [], [], 0) 
    if outerWallCount > 1:
        return False


    return True





# Randomly removes walls from the maze
def mazeRandomWallRemover(maze, removeCount, wallCoordinates): 

    for i in range(removeCount):

        #gets a wall from the selection pool
        randomWallCoordinate = random.choice(wallCoordinates) 
        randomRoomPos = randomWallCoordinate[0]
        randomDirection = randomWallCoordinate[1]


        #if one of the conditions is not met
        while not wallSandwhichFinder(maze, randomRoomPos, randomDirection):
            
            #removes the wall from the selection pool
            wallCoordinates.remove(randomWallCoordinate) 

            #gets a new wall from the selection pool
            randomWallCoordinate = random.choice(wallCoordinates) 
            randomRoomPos = randomWallCoordinate[0]
            randomDirection = randomWallCoordinate[1]


        #removes wall from maze if conditions are met
        maze.removeWall(randomRoomPos, randomDirection) 

        #removes the wall from the selection pool
        wallCoordinates.remove(randomWallCoordinate) 


    return maze



if __name__ == "__main__":
    mazeRandomizer()