import json
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


def evaluate():
    expected_answers_path = "/uufs/chpc.utah.edu/common/home/u1409693/independent-study/Phase1-I-O/val_I-O_2_shot.json"
    generated_answers_path = "/uufs/chpc.utah.edu/common/home/u1409693/output_I-O_2_shot_flan-t5-xxl.json"
    # expected_answers_path = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/validationPrompts.json"
    # generated_answers_path = "/Users/mugdha/Documents/IndependentStudy/movies/independent-study/output_answers.json"

    with open(expected_answers_path) as file:
        data_expected = json.load(file)
    with open(generated_answers_path) as file:
        data_generated = json.load(file)

    y_test = []
    for key in data_expected:
        if len(key) <= 10 and data_expected[key] == "negative":
            y_test.append(0)
        elif len(key) <= 10 and data_expected[key] == "positive":
            y_test.append(1)

    pred = [0 if val == "negative" else 1 for val in data_generated]

    precision = precision_score(y_test, pred)
    recall = recall_score(y_test, pred)
    accuracy = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred)

    print("Precision = ", precision)
    print("Recall = ", recall)
    print("Accuracy = ", accuracy)
    print("F1 score = ", f1)


evaluate()