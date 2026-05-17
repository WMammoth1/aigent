import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

	#sets variable absolute_path to the absolute path of the working directory
    working_dir_abs = os.path.abspath(working_directory)

        #constructs full path to the target directory by combining absolute path and directory argument,
        # normpath is called on the result to handle weirdness
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #validate target_dir falls within the absolute working_directory
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	#make sure file_path argument is a regular file
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'

	#check to see if file name ends in .py
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    try:
	#build command string and add args to command list
        command = ["python", target_dir]
        if args in command:
            command.extend(args)
        command_output = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_string = []
        if command_output.returncode != 0:
            return_code_value = command_output.returncode
            output_string.append(f'Process exited with code {return_code_value}')
            
        if command_output.stdout == "" and command_output.stderr == "":
            output_string.append("No output produced")
        if len(command_output.stdout) > 0:
            stdout_text = command_output.stdout
            output_string.append(f'STDOUT: {stdout_text}')
        if len(command_output.stderr) > 0:
            stderr_string = command_output.stderr
            output_string.append(f'STDERR: {stderr_string}')
        final_string = "\n".join(output_string)
        return final_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

#Gemini API function caller for run_python_file. Shows LLM how to call the function

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Allows LLM to run user-specified python code and returns results/errors",
        parameters=types.Schema(
                type=types.Type.OBJECT,
		required=["file_path"],
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="points to file location of python code to be processed"),
			"args": types.Schema(
				type=types.Type.ARRAY,
				description="optional arguments",
				items=types.Schema(
					type=types.Type.STRING,
					description="argument text"
					)
				)
			},
        	),
	)
        

