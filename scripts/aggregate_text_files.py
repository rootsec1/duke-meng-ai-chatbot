import os

DATA_DIR = "data/processed/cleaned"


def aggregate_text_files(data_dir):
    all_text = []
    for file in os.listdir(data_dir):
        with open(os.path.join(data_dir, file), "r") as f:
            all_text.append(f.read())
        all_text.append("\n")
    return all_text


def write_aggregated_text(all_text, output_file):
    with open(output_file, "w") as f:
        f.write("\n".join(all_text))


if __name__ == "__main__":
    all_text = aggregate_text_files(DATA_DIR)
    write_aggregated_text(all_text, "data/processed/context.txt")
    print("Aggregated text written to data/processed/context.txt")
