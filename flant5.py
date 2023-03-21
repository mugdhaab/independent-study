import argparse
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import json


def read_input(directory_path, directory_files):
    prompts = []
    for fileName in directory_files:
        file_path = directory_path + fileName
        with open(file_path, 'r') as file:
            data = file.read()
            prompts.append(data)
    return prompts


def run_model(prompts, shot):
    tokenizer = AutoTokenizer.from_pretrained("google/" + shot)
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
    model = AutoModelForSeq2SeqLM.from_pretrained("google/" + shot)
    outputs = model.generate(**inputs)
    answers = tokenizer.batch_decode(outputs, skip_special_tokens=True, max_length=5000)
    return answers


def output_formatting(output_answers, output_path):
    output_answers_trunc = [ans.strip().lower() for ans in output_answers]
    jsonString = json.dumps(output_answers_trunc)
    with open(output_path, "w") as outfile:
        outfile.write(jsonString)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="model size, supported: flan-t5-large, flan-t5-xl, flan-t5-xxl")
    parser.add_argument("--shot", type=int, help="Few shot, or Zero shot, supported: 0,1,2")
    parser.add_argument(
        "--task",
        type=str,
        help="Only answer (I-O), or answer with explanation (I-E-O), supported: I-O, I-E-O"
    )
    args = parser.parse_args()

    directory_path = "/uufs/chpc.utah.edu/common/home/u1409693/independent-study/" + "prompts_" + args.task + "_" + str(args.shot) + "_shot/"
    directory_files = sorted(os.listdir(directory_path))
    output_path = "/uufs/chpc.utah.edu/common/home/u1409693/output_" + args.task + "_" + str(args.shot) + "_shot.json"

    input_prompts = read_input(directory_path, directory_files)
    generated_answers = run_model(input_prompts, args.shot)
    output_formatting(generated_answers, output_path)
