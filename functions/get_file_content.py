from config import MAX_CHARS
import os
from google.genai import types

def get_file_content(working_directory, file_path):
	#sets variable absolute_path to the absolute path of the working directory
    working_dir_abs = os.path.abspath(working_directory)

        #constructs full path to the target directory by combining absolute path and directory argument,
        # normpath is called on the result to handle weirdness
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #validate target_dir falls within the absolute working_directory
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	#make sure file_path argument is a file
    if os.path.isfile(target_dir) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

	

	#try:
	#read the contents of the file and return a string
    with open(target_dir, "r") as f:
        file_content_string = f.read(MAX_CHARS)
                
	#check if the file was larger than the limit
        if f.read(1):
            file_content_string += f'[...File "{target_dir}" truncated at {MAX_CHARS} characters]'

      	#except Exception as e:
         #      	print(f"Error: {e}")		
	

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads file content and returns a string w/ a max of 10,000 characters",
        parameters=types.Schema(
                type=types.Type.OBJECT,
		required=["file_path"],
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="the destination file that is read from",
                        ),
                },
        ),
)

