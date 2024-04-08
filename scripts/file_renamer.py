import os

# Specify the directory path
directory_path = 'data/processed/cleaned'

# Iterate over all files in the directory
for filename in os.listdir(directory_path):
    # Construct the old file path
    old_file = os.path.join(directory_path, filename)
    
    # Check if it's a file and not a directory
    if os.path.isfile(old_file):
        # Construct the new file path with "external-" appended to the filename
        new_file = os.path.join(directory_path, "external-" + filename)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed "{filename}" to "external-{filename}"')

print("Renaming complete.")