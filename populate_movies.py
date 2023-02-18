from os import listdir
import csv
import jsonlines
import json


def populate_movies():
    # get list from docs
    # iterate 200 times
    # simulate 5 swaps
    # add to tsv
    mypath = "/Users/mugdha/Documents/Independent Study/movies/docs"
    allFiles = [f for f in sorted(listdir(mypath))]
    negReviews = allFiles[:1000]
    posReviews = allFiles[1000:]
    listMovies = []
    i = 0
    while i <= 499:
        cur_0 = i
        # cur_1 = i + 1
        # cur_2 = i + 2
        # cur_3 = i + 3
        i = i + 1
        curList = [negReviews[cur_0], posReviews[cur_0]]
        listMovies.append(curList)
        curList = [posReviews[cur_0], negReviews[cur_0]]
        listMovies.append(curList)

        # curList = [posReviews[cur_0], negReviews[cur_1], negReviews[cur_2], negReviews[cur_3],
        #            negReviews[cur_0], posReviews[cur_1], posReviews[cur_2], posReviews[cur_3]]
        # listMovies.append(curList)
        #
        # curList = [negReviews[cur_0], posReviews[cur_1], negReviews[cur_2], negReviews[cur_3],
        #            posReviews[cur_0], negReviews[cur_1], posReviews[cur_2], posReviews[cur_3]]
        # listMovies.append(curList)
        #
        # curList = [negReviews[cur_0], negReviews[cur_1], posReviews[cur_2], negReviews[cur_3],
        #            posReviews[cur_0], posReviews[cur_1], negReviews[cur_2], posReviews[cur_3]]
        # listMovies.append(curList)
        #
        # curList = [negReviews[cur_0], negReviews[cur_1], negReviews[cur_2], posReviews[cur_3],
        #            posReviews[cur_0], posReviews[cur_1], posReviews[cur_2], negReviews[cur_3]]
        # listMovies.append(curList)

    print(len(listMovies))
    print(len(listMovies[1]))
    print(listMovies[1])
    with open("train_movies.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        writer.writerows(listMovies)


def create_prompts():
    # import data from train.jsonl
    # pick the review text corresponding to each neg and pos and create a map
    # iterate over every row from csv and create the prompt
    # store every prompt in a new file
    trainPath = "/Users/mugdha/Documents/Independent Study/movies/train.jsonl"
    trainReviewsDict = {}
    with jsonlines.open(trainPath) as reader:
        for obj in reader:
            trainReviewsDict[obj["annotation_id"]] = obj["evidences"]

    valPath = "/Users/mugdha/Documents/Independent Study/movies/test.jsonl"
    valReviews = []
    with jsonlines.open(valPath) as reader:
        for obj in reader:
            valReviews.append(obj)

    json.dumps(trainReviewsDict)
    valDict = {}
    # print(len(trainReviewsDict))
    # print(trainReviewsDict["negR_004.txt"][0][0]['text'])
    # print(valReviews[0]['classification'])
    # print(valReviews[0]['evidences'][0][0]['text'])

    trainMoviesPath = "/Users/mugdha/Documents/Independent Study/movies/train_movies.csv"
    fileCount = 0
    valCount = 0
    with open(trainMoviesPath, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)

        curLoopNum = 1
        for review in list_of_csv:
            lines = []

            if curLoopNum % 7 == 0:
                valCount = valCount + 1
            curLoopNum = curLoopNum + 1
            countReviewLen = 0
            for i in range(2):
                # import the whole file text
                reviewText = []
                with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/docs/" + review[i], 'r') as file:
                    reviewText = file.read().replace('\n', '')

                line1 = "Question: Answer the following yes/no question."
                line2 = "Is this a positive movie review?"

                if countReviewLen + len(reviewText) > 150:
                    reviewText = reviewText[:150 - countReviewLen]
                line3 = "Review: " + reviewText
                if str(review[i]).startswith("neg"):
                    line4 = "A: no"
                else:
                    line4 = "A: yes"
                line5 = "###"
                lines.append(line1)
                lines.append(line2)
                lines.append(line3)
                lines.append(line4)
                lines.append(line5)
            lines.append(line1)
            lines.append(line2)
            # print(len(valReviews))
            # print(valReviews[valCount])
            # print(valReviews[valCount]['annotation_id'])
            with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/docs/" + valReviews[valCount]['annotation_id'], 'r') as file:
                valReviewText = file.read().replace('\n', '')
            lines.append("Review: " + valReviewText)
            lines.append("A:")
            if str(valReviews[valCount]['annotation_id']).startswith("neg"):
                valDict["prompt_" + str(fileCount)] = "no"
            else:
                valDict["prompt_" + str(fileCount)] = "yes"
            promptPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/prompts/prompt_" + str(fileCount) + ".txt"
            with open(promptPath, mode='wt', encoding='utf-8') as myFile:
                myFile.write('\n'.join(lines))
            with open("validationPrompts.json", "w") as outfile:
                json.dump(valDict, outfile)
            fileCount = fileCount + 1

        # add next line


# populate_movies()
create_prompts()
