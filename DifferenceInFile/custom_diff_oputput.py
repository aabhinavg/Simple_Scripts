import argparse
import re
import os

def extract_and_group_lines(input_file, output_file, custom_prefixes):
    try:
        # Open the input file for reading
        with open(input_file, "r") as f:
            # Read the content of the input file
            file_contents = f.read()

        # Create a dictionary to store prefixes and lists of corresponding file names
        prefix_suffix_mapping = {}

        for custom_prefix in custom_prefixes:
            # Construct a regular expression pattern that matches the custom prefix
            prefix_pattern = re.compile(rf'^{re.escape(custom_prefix)}\d?/.*', re.MULTILINE)
            custom_prefix_lines = re.findall(prefix_pattern, file_contents)

            for line in custom_prefix_lines:
                # Split the line by ':'
                parts = line.split(':')
                if len(parts) == 2:
                    # Get the prefix (part before ':')
                    prefix = parts[0]

                    # Get the file name (part after ':')
                    file_name = parts[1].strip()

                    # Check if the prefix is already in the dictionary
                    if prefix in prefix_suffix_mapping:
                        # If the prefix exists, add the file name to the list of suffixes
                        prefix_suffix_mapping[prefix].append(file_name)
                    else:
                        # If the prefix is new, create a list with the first file name
                        prefix_suffix_mapping[prefix] = [file_name]

        # Open the output file for writing
        with open(output_file, "w") as output:
            for prefix, suffixes in prefix_suffix_mapping.items():
                if len(suffixes) > 1:
                    # If there are multiple suffixes, print the prefix and all the suffixes
                    output.write(f"{prefix}: {', '.join(suffixes)}\n")
                else:
                    # If there is only one suffix, print the prefix and the single suffix
                    output.write(f"{prefix}: {suffixes[0]}\n")

        print(f"Extracted and grouped {len(prefix_suffix_mapping)} lines to {output_file}")

    except FileNotFoundError:
        print("Input file not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and group lines with custom prefixes from a file.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument(
        "--custom-prefixes", 
        help="Custom prefixes to match (comma-separated, e.g., 'Only in 2*,Only in 1*')",
        required=True
    )

    args = parser.parse_args()
    custom_prefixes = args.custom_prefixes.split(',')
    extract_and_group_lines(args.input_file, args.output_file, custom_prefixes)
