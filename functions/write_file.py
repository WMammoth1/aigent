import os

def write_file(working_directory, file_path, content):
    

     #sets variable absolute_path to the absolute path of the working directory
    working_dir_abs = os.path.abspath(working_directory)

        #constructs full path to the target directory by combining absolute path and directory argument,
        # normpath is called on the result to handle weirdness
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #validate target_dir falls within the absolute working_directory
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        #make sure file_path argument is a file
    if os.path.isdir(target_dir) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
	#creates missing parent directories of leaf (target_dir) if missing
        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

	#open file at target path in write mode and overwrite with content
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return (f"Error: {e}")

	#final content returned
    
