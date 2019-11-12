import random as random
import matplotlib.pyplot as plt

# Simulation Control Parameters

number_of_docs = 22560
prevalence_rate = 0.14 # target value
learning_rate = 400 # must be greater than training_signals
max_recall = 0.96
stopping_prev = 0.95 # will stop review

# Global Variables

docSet = []
recall = 0.5
training_signals = 100
foundTrend = []
aiReview = 0
prevalence = 0
confusion = []  # Cumulative list of tuples (tp, fp, tn, fn)


def initializeDocs():

    global number_of_docs
    global docSet
    global recall
    global prevalence_rate
    global prevalence

    responsiveDocs = 0

    for x in range(0,number_of_docs):
        r_tag = random.uniform(0,1)

        if r_tag < prevalence_rate:
            tag = 1
            responsiveDocs = responsiveDocs + 1
        else:
            tag = 0

        r_score = random.uniform(0,1)

        if tag == 1:

            if r_score < recall:
                score = 1
            else:
                score = 0

        else:

            if r_score < recall:
                score = 0
            else:
                score = 1

        doc = [tag,score]

        docSet.append(doc)

    prevalence = responsiveDocs
    print(f'Number of responsive docs: {prevalence}')

def getDocTag():
    global docSet

    actual = -1

    index = 0
    for doc in docSet:
        if doc[1] == 1:
            actual = doc[0]
            docSet.pop(index)
            break
        index = index + 1

    return actual

def rescore():
    global docSet
    global recall

    newDocSet = []

    for doc in docSet:
        r_score = random.uniform(0,1)

        if doc[0] == 1:

            if r_score < recall:
                score = 1
            else:
                score = 0

        else:

            if r_score < recall:
                score = 0
            else:
                score = 1

        newDoc = [doc[0],score]

        newDocSet.append(newDoc)

    docSet = newDocSet

def simulation():
    global found
    global foundTrend
    global recall
    global max_recall
    global learning_rate
    global docSet
    global prevalence
    global aiReview
    global stopping_prev
    global confusion

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    # Review documents scored as responsive
    aiReview = 1
    for x in range(0,number_of_docs):

        tag = getDocTag()

        # Record Findings
        if tag == -1 or tp + fn >= prevalence * stopping_prev:
            print(f'AI prioritized reviewed: {x}  Responsive found: {tp + fn}')
            break
        else:
            if tag == 1:
                tp += 1
            else:
                fp += 1
            confusion.append((tp, fp, 0, 0))

        # Re-score documents if AI is still training
        if x > 0 and x % training_signals == 0 and x <= learning_rate:
            recall = (max_recall - 0.5) * (x / learning_rate) + 0.5
            rescore()

        aiReview = aiReview + 1

    # Review remaining documents until requisite number of responsive are found
    linearReview = 0
    for doc in docSet:
        linearReview += 1
        if doc[0] == 1:
            fn += 1
        else:
            tn += 1

        if tp + fn >= prevalence * stopping_prev:
            print(f'Linear reviewed: {linearReview}')
            break

    totalReviewed = aiReview + linearReview
    print(f'Total reviewed: {totalReviewed}')
    print(f'Total found: {tp + fn}')
    reduction = (number_of_docs * stopping_prev - totalReviewed) / (number_of_docs * stopping_prev)
    print(f'Review Reduction: {reduction}')

def plotResults(listItems,title,y_axis,x_axis):


    plt.plot(listItems)
    plt.title(title)
    plt.ylabel(y_axis)
    plt.xlabel(x_axis)
    plt.show()

def stats():
    global confusion
    beta = 0.5

    runningPrecision = []
    runningRecall = []
    runningFScore = []

    for tp,fp,tn,fn in confusion:
        if tp + fp > 0:
            prec = tp / (tp + fp)
        else:
            prec = 0

        if tp + fn > 0:
            rec = tp / (tp+fn)
        else:
            rec = 0

        if prec > 0 or rec > 0:
            f_score = prec * rec / ((beta * beta * prec)+rec)
        else:
            f_score = 0

        runningPrecision.append(prec)
        runningRecall.append(rec)
        runningFScore.append(f_score)

    print(f'Last Precision: {runningPrecision[len(runningPrecision)-1]}')
    print(f'Last F-score: {runningFScore[len(runningFScore) - 1]}')

    return runningPrecision, runningRecall, runningFScore

def main():
    print(f'Number of Documents: {number_of_docs}')
    initializeDocs()
    simulation()
    runningPrecision, runningRecall, runningFScore = stats()
    plotResults(runningPrecision,'Running Precision','Precision (%)','Documents Reviewed')
    plotResults(runningFScore,'Running F-score','F-score Beta = 0.5 (%)','Documents Reviewed')
    plotResults(runningRecall, 'Running Recall', 'Recall (%)', 'Documents Reviewed')

main()

