import pandas as pd
import argparse
from tqdm import trange
import numpy as np
import os
import jsonlines
import random
from os import listdir
import json


def get_movies_examples(dataset_path, train_path, val_path, shot, task):
    """
    1. Creates prompts for both tasks (with explanation and without)
    2. Picks depending on number of examples to be used
    """
    # dataset_path = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/docs"
    # train_path = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/data_preprocessing/train.jsonl"
    # val_path = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/data_preprocessing/val.jsonl"
    allFiles = [f for f in sorted(listdir(dataset_path))]
    negReviews = allFiles[:200]
    posReviews = allFiles[1000:1200]
    review1 = negReviews[0]
    review2 = posReviews[0]

    trainReviewsDict = {}
    with jsonlines.open(train_path) as reader:
        for obj in reader:
            trainReviewsDict[obj["annotation_id"]] = obj["evidences"]

    valReviews = []
    with jsonlines.open(val_path) as reader:
        for obj in reader:
            valReviews.append(obj)

    # Selecting examples for the prompt depending on how many are needed for the experiment
    listMovies = []
    if shot == 1:
        train_prompts = [review1]
        for i in range(200):
            listMovies.append(train_prompts)
    elif shot == 2:
        train_prompts = [review1, review2]
        for i in range(200):
            random.shuffle(train_prompts)
            listMovies.append(train_prompts)

    # Creating prompts based on the task
    # if task == "I-O":
    line1 = "Question: Answer the following yes/no question."
    if task == "I-E-O":
        line1 = "Question: Answer the following yes/no question and report phrases in the review that are important for deciding on your answer."
    line2 = "Is this a positive movie review?"
    line3 = "Review: "
    line4 = "Important Phrases: "

    fileCount = 0
    valDict = {}

    for review in listMovies:
        lines = []
        for i in range(len(review)):
            with open(dataset_path + "/" + review[i], 'r') as file:
                reviewText = file.read().replace('\n', '')
            reviewTextList = reviewText.split(".")

            phrases = []
            impPhrasesLines = ""
            reviewLines = ""
            for reviewLine in reviewTextList:
                if task == "I-E-O":
                    for importantPhrase in trainReviewsDict[review[i]]:
                        if importantPhrase[0]['text'] in reviewLine:
                            phrases.append(importantPhrase[0]['text'])
                reviewLines += reviewLine + '. '
            if task == "I-E-O":
                impPhrasesLines += ", ".join(phrases)
            if str(review[i]).startswith("neg"):
                line5 = "Answer: no"
            else:
                line5 = "Answer: yes"
            line6 = "###"
            lines.append(line1)
            lines.append(line2)
            lines.append(line3 + reviewLines[:1000])
            if task == "I-E-O":
                lines.append(line4 + impPhrasesLines)
            lines.append(line5)
            lines.append(line6)
        lines.append(line1)
        lines.append(line2)

        '''
        Adding validation prompt
        '''
        with open(dataset_path + "/" + valReviews[fileCount]['annotation_id'], 'r') as file:
            valReviewText = file.read().replace('\n', '')
        lines.append("Review: " + valReviewText)
        if task == "I-O":
            lines.append("Answer:")
        elif task == "I-E-O":
            lines.append("Important Phrases:")

        '''
        Creating Val file
        '''
        if str(valReviews[fileCount]['annotation_id']).startswith("neg"):
            valDict["prompt_" + str(fileCount)] = "no"
        else:
            valDict["prompt_" + str(fileCount)] = "yes"

        if task == "I-E-O":
            importances = []
            for evidences in valReviews[fileCount]['evidences']:
                importances.append(evidences[0]['text'])
            valDict["prompt_" + str(fileCount) + "_imp_phrases"] = importances

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


def save_data():
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
