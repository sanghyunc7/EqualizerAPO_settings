import sys


class Flat_TXT:
    def __init__(self, input_file) -> None:
        self.file = input_file
        self.contents = []

    # unsorted output
    def flatten_equalizer(self, include_file):
        with open(include_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not line.startswith("#"):  # Skip commented-out lines
                    if line.startswith("Include:"):
                        child_file = line.split(": ")[1]
                        self.flatten_equalizer(child_file)
                    else:
                        self.contents.append(line)

    def sort_filters(self):
        new_contents = []
        for line in self.contents:
            if line.startswith("Filter:"):
                words = line.split()
                frequency = words[words.index("Hz") - 1]
                new_contents.append((float(frequency), line))
            else:
                new_contents.append((30000, line))
        new_contents.sort()
        self.contents = []
        for k, v in new_contents:
            self.contents.append(v)

    def get_flat(self):
        if self.contents:
            return self.contents
        self.flatten_equalizer(self.file)
        self.sort_filters()
        return self.contents


# def main():
#     input_file = sys.argv[1]
#     output_file = "flattened_" + input_file
#     flat_contents = flatten_equalizer(input_file)
#     print(flat_contents)
#     flat_contents = sort_filters(flat_contents)
#     print(flat_contents)
#     with open(output_file, 'w') as f:
#         for line in flat_contents:
#             f.write(line + '\n')


# if __name__ == "__main__":
#     main()
