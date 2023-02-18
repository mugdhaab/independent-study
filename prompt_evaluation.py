from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import json
import os

directory_path = '/Users/mugdha/Documents/Independent Study/movies/independent-study/prompts/'
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
    inputs = tokenizer(prompts[:10], return_tensors="pt", padding=True, truncation=True)
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
    outputs = model.generate(**inputs)
    answers = tokenizer.batch_decode(outputs, skip_special_tokens=True, max_length=5000)
    return answers


def output_formatting(output_answers):
    output_answers_trunc = [ans[3:6].strip().lower() for ans in output_answers]
    jsonString = json.dumps(output_answers_trunc)
    with open("/Users/mugdha/Documents/Independent Study/movies/independent-study/output_answers.json", "w") as outfile:
        outfile.write(jsonString)


input_prompts = read_input()
generated_answers = run_model(input_prompts)
output_formatting(generated_answers)
