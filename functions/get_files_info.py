import os

def get_files_info(working_directory, directory="."):
	#sets variable absolute_path to the absolute path of the working directory
	working_dir_abs = os.path.abspath(working_directory)
	
	#constructs full path to the target directory by combining absolute path and directory argument,
	# normpath is called on the result to handle weirdness
	target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

	#validate target_dir falls within the absolute working_directory
	if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
	#make sure directory argument is a directory (string)
	if os.path.isdir(target_dir) == False:
		return f'Error: "{directory}" is not a directory'

	#record the name, file size, and whether it's a directory
	lines = []
	for file in os.listdir(target_dir):
		full_path = os.path.join(target_dir, file)
		try:
			name = file
			size = os.path.getsize(full_path)
			dir = os.path.isdir(full_path)
		except Exception as e:
			print(f"Error: {e}")

		lines.append(f"  - {name}: file_size={size} bytes, is_dir={dir}")
	return "\n".join(lines)
				
get_files_info("calculator", ".")
get_files_info("calculator", "pkg")
get_files_info("calculator", "/bin")
get_files_info("calculator", "../")


