import pandas as pd

csv_file = "csv_file.csv"
output_nlu = "nlu.yml"
output_domain = "domain.yml"
output_stories = "stories.yml"

def main():
    data = pd.read_csv(csv_file)

    unique_intents = set()
    unique_responses = {}
    stories = {}
    generated_stories = set()

    for index, row in data.iterrows():
        story_id = row["story_id"] if not pd.isna(row["story_id"]) else f"default_story_{index}"
        user_message, reply, intent = row["user_message"], row["reply"], row["intent"]
        unique_intents.add(intent)

        if intent not in unique_responses:
            unique_responses[intent] = reply

        if story_id not in stories:
            stories[story_id] = []

        stories[story_id].append((intent, user_message))

    with open(output_nlu, "w", encoding="utf-8") as nlu_out:
        nlu_out.write("version: \"3.1\"\n")
        nlu_out.write("nlu:\n")

        for intent in unique_intents:
            nlu_examples = "\n".join([f"    - {example}" for story_id in stories for intent_name, example in stories[story_id] if intent_name == intent])
            nlu_out.write(f"- intent: {intent}\n")
            nlu_out.write("  examples: |\n")
            nlu_out.write(nlu_examples + "\n\n")

    with open(output_domain, "w", encoding="utf-8") as domain_out:
        domain_out.write("version: \"3.1\"\n")
        domain_out.write("intents:\n")
        domain_out.write("\n".join([f"  - {intent}" for intent in unique_intents]) + "\n")

        domain_out.write("responses:\n")
        for intent, reply in unique_responses.items():
            domain_out.write(f"  utter_{intent}:\n")
            domain_out.write(f"  - text: \"{reply}\"\n")

    with open(output_stories, "w", encoding="utf-8") as stories_out:
        stories_out.write("version: \"3.1\"\n")
        stories_out.write("stories:\n")

        for story_id, story in stories.items():
            story_str = "\n".join([f"  - intent: {intent}\n  - action: utter_{intent}" for intent, _ in story])

            if story_str not in generated_stories:
                stories_out.write(f"- story: conversation {story_id}\n")
                stories_out.write("  steps:\n")
                stories_out.write(story_str + "\n\n")
                generated_stories.add(story_str)

if __name__ == "__main__":
    main()
