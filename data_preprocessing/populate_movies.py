from os import listdir
import csv
import jsonlines
import json
import random


def populate_movies():
    mypath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/docs"
    allFiles = [f for f in sorted(listdir(mypath))]
    negReviews = allFiles[:200]
    posReviews = allFiles[1000:1200]

    listMovies = []
    for i in range(200):
        curList = [negReviews[i], posReviews[i]]
        random.shuffle(curList)
        listMovies.append(curList)

    with open("train_movies.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        writer.writerows(listMovies)


def create_prompts():
    # import data from train.jsonl
    # pick the review text corresponding to each neg and pos and create a map
    # iterate over every row from csv and create the prompt
    # store every prompt in a new file
    trainPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/data_preprocessing/train.jsonl"
    # negR_004.txt : [
    trainReviewsDict = {}
    with jsonlines.open(trainPath) as reader:
        for obj in reader:
            trainReviewsDict[obj["annotation_id"]] = obj["evidences"]

    valPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/data_preprocessing/val.jsonl"
    valReviews = []
    with jsonlines.open(valPath) as reader:
        for obj in reader:
            valReviews.append(obj)

    json.dumps(trainReviewsDict)

    valDict = {}

    trainMoviesPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/data_preprocessing/train_movies.csv"
    fileCount = 0

    with open(trainMoviesPath, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)

        for review in list_of_csv:
            lines = []
            for i in range(2):
                # import the whole file text
                # reviewText = []
                with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/docs/" + review[i],
                          'r') as file:
                    reviewText = file.read().replace('\n', '')

                line1 = "Question: Answer the following yes/no question and report phrases in the review that are important for deciding on your answer."
                line2 = "Is this a positive movie review?"
                line3 = "Review: "
                line4 = "Important Phrases: "

                phrases = []
                reviewTextList = reviewText.split(".")

                for reviewLine in reviewTextList:
                    for importantPhrase in trainReviewsDict[review[i]]:
                        if importantPhrase[0]['text'] in reviewLine:
                            phrases.append(importantPhrase[0]['text'])
                    line3 += reviewLine + '. '

                line4 += ", ".join(phrases)
                if str(review[i]).startswith("neg"):
                    line5 = "Answer: no"
                else:
                    line5 = "Answer: yes"
                line6 = "###"
                lines.append(line1)
                lines.append(line2)
                lines.append(line3[:1000])
                lines.append(line4)
                lines.append(line5)
                lines.append(line6)
            lines.append(line1)
            lines.append(line2)

            # print(len(valReviews))
            # print(valReviews[valCount])
            # print(valReviews[valCount]['annotation_id'])

            '''
            Adding validation prompt
            '''
            with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/docs/" + valReviews[fileCount]['annotation_id'], 'r') as file:
                valReviewText = file.read().replace('\n', '')
            lines.append("Review: " + valReviewText)
            # lines.append("Answer:")
            lines.append("Important Phrases:")

            '''
            Creating Val file
            '''
            if str(valReviews[fileCount]['annotation_id']).startswith("neg"):
                valDict["prompt_" + str(fileCount)] = "no"
            else:
                valDict["prompt_" + str(fileCount)] = "yes"

            importances = []
            for evidences in valReviews[fileCount]['evidences']:
                importances.append(evidences[0]['text'])
            valDict["prompt_" + str(fileCount) + "_imp_phrases"] = importances

            with open("validationPromptsImpPhrases.json", "w") as outfile:
                json.dump(valDict, outfile)

            '''
            Creating prmopt file
            '''
            promptPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/prompts_important/prompt_" + str(fileCount) + ".txt"
            with open(promptPath, mode='wt', encoding='utf-8') as myFile:
                myFile.write('\n'.join(lines))

            fileCount = fileCount + 1

        # add next line


# populate_movies()
create_prompts()

# "[This is a great day, It could have been a great day, I am loving it, Play basketball with me,
# Mangoes are better than oranges, Life is awesome]"
# ["basketball with", "great day"]

# 150 tokens
# Output: "This is a great day. It could have been a great day. Play basketball with me. Mangoes are better than"
# 150 - number of tokens in output
