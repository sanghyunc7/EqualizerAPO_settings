import sys

def flatten_equalizer(file_path):
    flat_contents = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):  # Skip commented-out lines
                if line.startswith('Include:'):
                    include_file = line.split(': ')[1]
                    included_contents = flatten_equalizer(include_file)
                    flat_contents.extend(included_contents)
                else:
                    flat_contents.append(line)
    return flat_contents


def sort_filters(contents):
    new_contents = []
    for line in contents:
        if line.startswith("Filter:"):
            words = line.split()
            frequency = words[words.index('Hz') - 1]
            new_contents.append((float(frequency), line))
        else:
            new_contents.append((0, line))
    new_contents.sort()
    rtn = []
    for k,v in new_contents:
        rtn.append(v)
    return rtn


def main():
    input_file = sys.argv[1]
    output_file = "flattened_" + input_file
    flat_contents = flatten_equalizer(input_file)
    print(flat_contents)
    flat_contents = sort_filters(flat_contents)
    print(flat_contents)
    with open(output_file, 'w') as f:
        for line in flat_contents:
            f.write(line + '\n')






if __name__ == "__main__":
    main()
