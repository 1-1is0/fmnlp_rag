import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()
import yaml

just_one = False
llm_right = 0
rag_right = 0
total = 0
with open('output.yaml', 'r') as yaml_file:
    data_list = yaml.load(yaml_file, Loader=yaml.FullLoader)
    for data in data_list:
        question = data["question"].lower()
        answers = data["answers"]
        llm = data["llm"].lower()
        rag = data["rag"].lower()

        for ans in answers:
            if ans.lower() in llm:
                llm_right += 1
                # break
                if just_one:
                    break

        for ans in answers:
            if ans.lower() in rag:
                rag_right += 1
                # break
                if just_one:
                    break
        if just_one:
            total += 1
        else:
            total += len(answers)

print("total", total)
print("llm_right", llm_right, llm_right/total)
print("rag_right", rag_right, rag_right/total)

