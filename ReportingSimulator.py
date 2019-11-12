import numpy as np
import random as random
import matplotlib.pyplot as plt


print("MULTIVERSE")

# USER ACTIONS

# (I) Ingest

# (C) Cull
# - Document count to cull
# - Universes affected

# (U) Universe

# (M) Merge Universes

# (T) Tag Documents

# (UT) Untag Documents
# - Universes affected
# - Tags to remove

# (Q) Quit


# DATA MODEL

class Matter:
    documents = []
    universes = []
    tagEvents = []

class Document:
    def __init__(self, docID,tags):
        self.docID = docID
        self.tags = tags
        self.universes = []

class TagEvent:
    def __init__(self, docID,tag,tagState,tagEventDateTime,isRandom):
        self.docID = docID
        self.tag = tag
        self.tagState = tagState
        self.tagEventDateTime = tagEventDateTime
        self.isRandom = isRandom

class Universe:
    def __init__(self, universeID,targetConfidenceLevel,targetMarginOfError):
        self.universeID = universeID
        self.targetConfidenceLevel = targetConfidenceLevel
        self.targetMarginOfError = targetMarginOfError

# USER INTERACTIONS

def status():
    print()
    print("============================================================")
    print("Commands: I, C, U, M, T, UT, Q")

def ingest(matter):
    ingestCount = input("Number of documents to ingest: ")
    print()
    ingestCount = int(ingestCount)
    global totalDocs

    #Distribution of tags
    # Random float x, 0.0 <= x < 1.0
    dist_a = random.random()
    dist_b = random.random()
    dist_c = random.random()
    dist_ab = random.random()
    dist_ac = random.random()
    dist_bc = random.random()
    dist_abc = random.random()
    dist_total = dist_a + dist_b + dist_c + dist_ab + dist_ac + dist_bc + dist_abc
    count_a = round(ingestCount * dist_a / dist_total)
    count_b = round(ingestCount * dist_b / dist_total)
    count_c = round(ingestCount * dist_c / dist_total)
    count_ab = round(ingestCount * dist_ab / dist_total)
    count_ac = round(ingestCount * dist_ac / dist_total)
    count_bc = round(ingestCount * dist_bc / dist_total)
    count_abc = round(ingestCount * dist_abc / dist_total)

    for x in range(count_a):
        totalDocs = totalDocs+1
        newDoc = Document(totalDocs,["responsive"])
        matter.documents.append(newDoc)

    for x in range(count_b):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["hot"])
        matter.documents.append(newDoc)

    for x in range(count_c):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["junk"])
        matter.documents.append(newDoc)

    for x in range(count_ab):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["responsive", "hot"])
        matter.documents.append(newDoc)

    for x in range(count_ac):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["responsive","junk"])
        matter.documents.append(newDoc)

    for x in range(count_bc):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["hot","junk"])
        matter.documents.append(newDoc)

    for x in range(count_abc):
        totalDocs = totalDocs + 1
        newDoc = Document(totalDocs, ["responsive","hot","junk"])
        matter.documents.append(newDoc)

    # Randomize order of documents
    random.shuffle(matter.documents)

    print('The distribution of ingested documents is: ')
    print('Responsive: \t\t\t\t',str(count_a))
    print('Hot: \t\t\t\t\t\t', str(count_b))
    print('Junk: \t\t\t\t\t\t', str(count_c))
    print('Responsive and Hot: \t\t', str(count_ab))
    print('Responsive and Junk: \t\t', str(count_ac))
    print('Hot and Junk: \t\t\t\t', str(count_bc))
    print('Responsive, Hot, and Junk: \t', str(count_abc))

    print()
    print('Total documents in matter',str(totalDocs))

def makeUniverse(matter):
    global totalDocs
    global universeID
    universeSize = input('Number of documents in universe: ')
    tgtConf = input('Target confidence level as decimal: ')
    tgtMarg = input('Target margin of error as decimal: ')

    if int(universeSize) > totalDocs:
        print('ERROR: universe size is larger than documents in review database.')
    else:
        universeID = universeID + 1
        newUniverse = Universe(universeID,tgtConf,tgtMarg)
        matter.universes.append(newUniverse)
        docCounter = 0
        for myDoc in matter.documents:
            docCounter = docCounter + 1
            if docCounter <= int(universeSize):
                myDoc.universes.append(universeID)
        print('Review universe ID ', str(universeID), ' has been created.')

    random.shuffle(matter.documents)

def inUniverse(myDoc,universeInterest):

    match = False

    for myUniv in myDoc.universes:
        for myUnivInterest in universeInterest:
            if myUniv == int(myUnivInterest):
                match = True

    return match

def notReviewed(tagEvents, myDoc, tagInterest):

    isNotReviewed = True

    match = []
    for myTagInterest in tagInterest:
        isTagged = False
        for myEvent in tagEvents:
            if myTagInterest == myEvent.tag:
                if myEvent.tagState == 'applied' or myEvent.tagState == 'notApplied':
                    isTagged = True
                else:
                    isTagged = False
        match.append(isTagged)
    for item in match:
        if item == False:
            isNotReviewed = True
    return isNotReviewed

def prioritizeCandidates(matter, candidateDocs, tagInterest):
    docsInList = len(candidateDocs)

    taggedDocs = []
    untaggedDocs = []
    enrichedList = []

    # tempTaggedDocs = []

    for x in range(1,docsInList):
        for myDoc in matter.documents:
            if myDoc.docID == candidateDocs[x]:
                hasTag = False
                for myTag in myDoc.tags:
                    for myTagInterest in tagInterest:
                        if myTag == myTagInterest:
                            hasTag = True
                if hasTag:
                    taggedDocs.append(myDoc.docID)
                    # tempTaggedDocs.append(myDoc.docID)
                else:
                    untaggedDocs.append(myDoc.docID)

    # boolList = []
    # for myID in candidateDocs:
    #     isInList = False
    #     for myTagDoc in tempTaggedDocs:
    #         if myID == myTagDoc:
    #             isInList = True
    #     if isInList:
    #         boolList.append("Y")
    #     else:
    #         boolList.append("n")
    # print("pre enrichment: ",boolList)

    while len(taggedDocs) > 0 or len(untaggedDocs) > 0:
        r = random.random()
        if r < 0.95:
            if len(taggedDocs) > 0:
                enrichedList.append(taggedDocs[0])
                taggedDocs.pop(0)
            else:
                enrichedList.append(untaggedDocs[0])
                untaggedDocs.pop(0)
        else:
            if len(untaggedDocs) > 0:
                enrichedList.append(untaggedDocs[0])
                untaggedDocs.pop(0)
            else:
                enrichedList.append(taggedDocs[0])
                taggedDocs.pop(0)

    # boolList = []
    # for myID in enrichedList:
    #     isInList = False
    #     for myTagDoc in tempTaggedDocs:
    #         if myID == myTagDoc:
    #             isInList = True
    #     if isInList:
    #         boolList.append("Y")
    #     else:
    #         boolList.append("n")
    # print("post enrichment: ", boolList)

    return enrichedList

def tagByPriority(matter,candidateDocs,priorityTag,reviewCount,tagInterest):

    global taggingSession

    print('Candidate docs initial: ', candidateDocs)

    if priorityTag == "":
        random.shuffle(candidateDocs)
        print('Candidate docs randomized: ', candidateDocs)
        isRandom = True
    else:
        candidateDocs = prioritizeCandidates(matter, candidateDocs, tagInterest)
        print('Candidate docs prioritized: ', candidateDocs)
        isRandom = False

    for myTag in tagInterest:
        reviewedDocs = 0
        for myDocID in candidateDocs:
            if reviewedDocs <= reviewCount:
                for myDoc in matter.documents:
                    if myDoc.docID == myDocID:
                        isTagged = False
                        for myEvent in matter.tagEvents:
                            if myEvent.tag == myTag:
                                if myEvent.tagState == 'applied' or myEvent.tagState == 'notApplied':
                                    isTagged = True
                        if isTagged == False:
                            toApply = False
                            for truthTag in myDoc.tags:
                                if truthTag == myTag:
                                    toApply = True
                            if toApply:
                                taggingSession = taggingSession + 1
                                newTagEvent = TagEvent(myDoc.docID,myTag,'applied',taggingSession,isRandom)
                                matter.tagEvents.append((newTagEvent))
                                reviewedDocs = reviewedDocs + 1
                            else:
                                taggingSession = taggingSession + 1
                                newTagEvent = TagEvent(myDoc.docID, myTag, 'notApplied', taggingSession,isRandom)
                                matter.tagEvents.append((newTagEvent))
                                reviewedDocs = reviewedDocs + 1

def tagDocs(matter):
    global universeID
    global totalDocs

    # Get information from user
    print('Enter the number of documents to review between 1 and ',str(totalDocs),".")
    reviewCount = input('Number to review: ')
    reviewCount = int(reviewCount)
    tagInterest = input('Enter tags that will be considered separated by spaces: ')
    tagInterest = tagInterest.split()
    print('Review universe ID range from 1 to ',str(universeID),".")
    universeInterest = input('Enter universe ID of interest separated by spaces: ')
    universeInterest = universeInterest.split()
    priorityTag = input('Tag by which to prioritize: ')

    # Build list of tagging candidates
    candidateDocs = []

    for myDoc in matter.documents:
        if inUniverse(myDoc,universeInterest) and notReviewed(matter.tagEvents, myDoc, tagInterest):
            candidateDocs.append(myDoc.docID)

    tagByPriority(matter,candidateDocs,priorityTag,reviewCount,tagInterest)

    # Generate review report
    # Report on how many documents were tagged for each tag

def cull():
    cullCount = input("Number of documents to cull: ")

def plotGainCurve(matter):

    chosenUniverse = input("Universe to plot: ")

    # Cycle through each tagging session time
    # Cycle through each tagEvent
    # If session time same as event then
    #
    # Cycle through each document
    # If document in universe
    #

    x = np.arange(0, 5, 0.1);
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()

# MAIN PROGRAM

totalDocs = 0
universeID = 0
taggingSession = 0

matter = Matter()
var1 = ""

while var1 != "q" and var1 != "Q":

    status()

    var1 = input("Action: ")

    if var1 == "I" or var1 == "i":
        ingest(matter)

    if var1 =="U" or var1 == "u":
        makeUniverse(matter)

    if var1 =="T" or var1 == "t":
        tagDocs(matter)

    if var1 == "C" or var1 == "c":
        cull()

    if var1 == "P" or var1 == "p":
        plotGainCurve()

print("END OF PROGRAM")



