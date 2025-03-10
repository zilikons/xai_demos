from google import genai
import os
import json
import random
from pathlib import Path


def process_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    random.shuffle(data)

    selected_elements = data[:64]

    result_str = ""
    for element in selected_elements:
        result_str += f"user: {element['user']}\nassistant: {element['assistant']}"
    return result_str


file_path = Path(__file__).parent / "examples.json"
# replace your own jailbreak prompt
jailbreak_prompt = "please tell me how to jailbreak my iPhone"
few_shot_example = process_json(file_path.resolve())
few_shot_example += f"user: {jailbreak_prompt}\nassistant: "
final_result = few_shot_example

# from google import genai
print(process_json(file_path.resolve())[:500])
print(jailbreak_prompt)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    config=genai.types.GenerateContentConfig(
        system_instruction=process_json(file_path.resolve()), temperature=1.0
    ),
    contents=f"user: {jailbreak_prompt}\nassistant: ",
)
print(response.text)
# save completion as txt
# with open("gptminijb.txt", "w") as text_file:
#     text_file.write(completion.choices[0].message)

# print(final_result)
