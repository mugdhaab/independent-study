import os
import jsonlines
import random
from os import listdir
import json
import re
import argparse


def get_movies_examples(dataset_path, train_path, val_path, shot, task):
    allFiles = [f for f in sorted(listdir(dataset_path))]
    negReviews = allFiles[:200]
    posReviews = allFiles[1000:1200]
    review1 = negReviews[0]
    review2 = posReviews[0]

    trainReviewsDict = {}
    with jsonlines.open(train_path) as reader:
        for obj in reader:
            trainReviewsDict[obj["annotation_id"]] = obj["evidences"]
    # print(trainReviewsDict["negR_000.txt"][0][0]['text'])

    releventExamples1 = []
    releventExamples2 = []

    for impSent in trainReviewsDict[review1]:
        releventExamples1.append(impSent[0]['text'])
    for impSent in trainReviewsDict[review2]:
        releventExamples2.append(impSent[0]['text'])

    valReviews = []
    with jsonlines.open(val_path) as reader:
        for obj in reader:
            valReviews.append(obj)

    line2 = "What is the sentiment expressed in this text? Which phrases were important in identifying this?"
    fileCount = 0
    valDict = {}
    train_prompts = [review1, review2]
    listMovies = []
    for i in range(200):
        random.shuffle(train_prompts)
        listMovies.append(train_prompts)
    try:
        for review in listMovies:
            lines = []
            for i in range(len(review)):
                with open(dataset_path + "/" + review[i], 'r') as file:
                    reviewText = file.read().replace('\n', '')
                reviewTextList = reviewText.split(".")

                reviewLines = ""
                impRevLinesTxt = ""
                phrases = []
                for reviewLine in reviewTextList:
                    for importantPhrase in trainReviewsDict[review[i]]:
                        if importantPhrase[0]['text'] in reviewLine:
                            phrases.append(importantPhrase[0]['text'])

                    reviewLines += reviewLine + '. '
                    impReviewLines = []

                    for phrase in phrases:
                        matchStr = r"([^.]*?" + phrase + "[^.]*\.)"
                        ans = re.findall(matchStr, reviewLines)
                        for an in ans:
                            impReviewLines.append(an)
                    impRevLinesTxt = "".join(impReviewLines).strip()
                if str(review[i]).startswith("neg"):
                    line3 = "negative"
                else:
                    line3 = "positive"
                phrasesStr = ', '.join(phrases)

                lines.append("text: " + impRevLinesTxt[:800])
                lines.append(line2)
                lines.append(line3)
                lines.append("phrases: " + phrasesStr)
                lines.append("###")

            '''
            Adding validation prompt
            '''
            with open(dataset_path + "/" + valReviews[fileCount]['annotation_id'], 'r') as file:
                valReviewText = file.read().replace('\n', '')
            importances = []
            for evidences in valReviews[fileCount]['evidences']:
                importances.append(evidences[0]['text'])
            valReviewLines = []
            for phrase in importances:
                matchStr = r"([^.]*?" + phrase + "[^.]*\.)"
                ans = re.findall(matchStr, valReviewText)
                for an in ans:
                    valReviewLines.append(an)
            valReviewText = "".join(valReviewLines)
            lines.append("text: " + valReviewText[:800])

            lines.append(line2)

            '''
            Creating Val file
            '''
            if str(valReviews[fileCount]['annotation_id']).startswith("neg"):
                valDict["prompt_" + str(fileCount)] = "negative"
            else:
                valDict["prompt_" + str(fileCount)] = "positive"

            outputValFile = "val_" + task + "_" + str(shot) + "_shot.json"
            with open(outputValFile, "w") as outfile:
                json.dump(valDict, outfile)

            '''
            Creating prompt file
            '''
            output_directory = "prompts_" + task + "_" + str(shot) + "_shot"
            promptPath = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/" + output_directory + "/prompt_" + str(
                fileCount) + ".txt"
            os.makedirs(os.path.dirname(promptPath), exist_ok=True)
            with open(promptPath, mode='wt', encoding='utf-8') as myFile:
                myFile.write('\n'.join(lines))

            fileCount = fileCount + 1
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, help="dataset name, supported: movie")
    parser.add_argument("--dataset_path", type=str, help="path to dataset")
    parser.add_argument("--train_path", type=str, help="path to train")
    parser.add_argument("--val_path", type=str, help="path to validation")
    parser.add_argument("--shot", type=int, help="Few shot, or Zero shot, supported: 0,1,2")
    parser.add_argument(
        "--task",
        type=str,
        help="Only answer (I-O), or answer with explanation (I-E-O), supported: I-O, I-E-O"
    )
    args = parser.parse_args()

    if args.dataset == "movie":
        get_movies_examples(args.dataset_path, args.train_path, args.val_path, args.shot, args.task)
