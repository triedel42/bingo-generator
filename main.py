from pdf import generate_bingo_pdf
import csv
import yaml
import random


def generate_single_bingo(event_pool: list[dict], partic_name, file_name, min_upvotes=1):
    pool_strings: list[str] = [f"{e['event']}" for e in event_pool if int(e["upvotes"]) >= min_upvotes]
    # weights = [float(e["upvotes"]) for e in event_pool]
    event_sample = random.sample(pool_strings, k=24)
    random.shuffle(event_sample)
    generate_bingo_pdf(file_name, event_sample, identifier=partic_name)


def generate_all(file_name, file_name_config):
    with open(file_name_config, "r") as f:
        participants: list[str] = yaml.safe_load(f)["participants"]

    with open(file_name, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        event_pool = []
        for row in reader:
            event_pool.append(row)

    for p in participants:
        generate_single_bingo(event_pool, p, f"sheets/{p}.pdf")


if __name__ == "__main__":
    generate_all("events.csv", "config.yaml")
    print("done.")
