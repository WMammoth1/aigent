import os
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from functions.get_file_content import get_file_content
from call_function import available_functions, call_function

def main():
    
	load_dotenv()
	
	#retrieves Google Gemini API key for Gemini AI Studio from .env and sets to variable api_key
	api_key = os.environ.get('GEMINI_API_KEY')

	if api_key == None:
		raise RuntimeError("environmental variable was not found")

	client = genai.Client(api_key=api_key)
	
	#creates positional argument for argparse to use with user generated input, accessed with args.user_prompt
	parser = argparse.ArgumentParser(description="Genai Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()

	# creates a new list of types.content and set's user's prompt as message, note types imported from google.genai
	messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

	for i in range(20):

		response = client.models.generate_content(
			model='gemini-2.5-flash',
			contents=messages,
			config=types.GenerateContentConfig(
				tools=[available_functions],
				system_instruction=system_prompt,
				temperature=0),
    		)
	
		for candidate in response.candidates:
			messages.append(candidate.content)		

		usage_metadata = response.usage_metadata

		if usage_metadata is None:
			raise RuntimeError("failed API request")

	
		user_prompt = args.user_prompt
		prompt_tokens = usage_metadata.prompt_token_count
		response_tokens = usage_metadata.candidates_token_count

	
		if args.verbose:
			print(f"User prompt: {user_prompt}")
			print(f"Prompt tokens: {prompt_tokens}")
			print(f"Response tokens: {response_tokens}")
	
	
		if response.function_calls:
					
			function_results_list = []
			for function_call in response.function_calls:
				function_call_result = call_function(function_call, args)

				if not function_call_result.parts:
					raise Exception
				
	
				if function_call_result.parts[0].function_response == None:
					raise Exception

				if function_call_result.parts[0].function_response.response == None:
					raise Exception
			
				function_results_list.append(function_call_result.parts[0])
				
				if args.verbose == True:
					print(f"-> {function_call_result.parts[0].function_response.response}")

			messages.append(types.Content(role="user", parts=function_results_list))	
		

		else:
			print(f"{response.text}")
			return
	
if __name__ == "__main__":
	main()

