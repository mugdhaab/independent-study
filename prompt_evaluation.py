from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import json
import os

directory_path = '/uufs/chpc.utah.edu/common/home/u1409693/independent-study/prompts_important/'
directory_files = sorted(os.listdir(directory_path))


def read_input():
    prompts = []
    for fileName in directory_files:
        file_path = directory_path + fileName
        with open(file_path, 'r') as file:
            data = file.read()
            prompts.append(data)
    return prompts


def run_model(prompts):
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
    outputs = model.generate(**inputs)
    answers = tokenizer.batch_decode(outputs, skip_special_tokens=True, max_length=5000)
    return answers


def output_formatting(output_answers):
    output_answers_trunc = [ans[3:6].strip().lower() for ans in output_answers]
    jsonString = json.dumps(output_answers_trunc)
    with open("/uufs/chpc.utah.edu/common/home/u1409693/independent-study/output_answers_important.json", "w") as outfile:
        outfile.write(jsonString)


input_prompts = read_input()
generated_answers = run_model(input_prompts)
output_formatting(generated_answers)
