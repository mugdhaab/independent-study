from os import listdir
import csv
import jsonlines
import json


def zero_shot_prompts():
    valPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/data_preprocessing/val.jsonl"
    valReviews = []
    with jsonlines.open(valPath) as reader:
        for obj in reader:
            valReviews.append(obj)
    valDict = {}
    for valCount in range(len(valReviews)):
        lines = []
        line1 = "Question: Answer the following yes/no question."
        line2 = "Is this a positive movie review?"
        lines.append(line1)
        lines.append(line2)
        with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/docs/" + valReviews[valCount][
            'annotation_id'], 'r') as file:
            valReviewText = file.read().replace('\n', '')
        lines.append("Review: " + valReviewText)

        line3 = "Answer:"
        lines.append(line3)

        # importances = []
        # for evidences in valReviews[valCount]['evidences']:
        #     importances.append(evidences[0]['text'])

        # valDict["prompt_" + str(valCount) + "_imp_phrases"] = importances


        promptPath = "/Users/mugdha/Documents/Independent Study/movies/independent-study/prompts_zero_shot/prompt_" + str(
            valCount) + ".txt"
        with open(promptPath, mode='wt', encoding='utf-8') as myFile:
            myFile.write('\n'.join(lines))

        if str(valReviews[valCount]['annotation_id']).startswith("neg"):
            valDict["prompt_" + str(valCount)] = "no"
        else:
            valDict["prompt_" + str(valCount)] = "yes"

        with open("validationPromptsZeroShot.json", "w") as outfile:
            json.dump(valDict, outfile)


zero_shot_prompts()
