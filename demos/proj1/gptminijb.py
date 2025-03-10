import openai
import os
import json
import random
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")


def process_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    random.shuffle(data)

    selected_elements = data[:512]

    result_list = []
    for element in selected_elements:
        result_dict = {}
        result_dict["role"] = "user"
        result_dict["content"] = (
            f"user: {element['user']}\nassistant: {element['assistant']}"
        )
        result_list.append(result_dict)
    return result_list


file_path = Path(__file__).parent / "examples.json"
# replace your own jailbreak prompt
jailbreak_prompt = "user: please tell me how to jailbreak my iPhone"
few_shot_example = process_json(file_path.resolve())
few_shot_example.append(
    {"role": "user", "content": f"user: {jailbreak_prompt}\nassistant: "}
)
final_result = few_shot_example
print(type(final_result[0]))
client = openai.OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=final_result,
    logprobs=True,
    top_logprobs=5,
    store=True,
)

print(completion)
# save completion as txt
# with open("gptminijb.txt", "w") as text_file:
#     text_file.write(completion.choices[0].message)

# print(final_result)
