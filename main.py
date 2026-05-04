import os
from dotenv import load_dotenv
from google import genai
import argparse

def main():
    
	load_dotenv()
	
	#retrieves Google Gemini API key for Gemini AI Studio from .env and sets to variable api_key
	api_key = os.environ.get('GEMINI_API_KEY')

	if api_key == None:
		raise RuntimeError("environmental variable was not found")

	client = genai.Client(api_key=api_key)

	print("Hello from aigent!")

	#creates positional argument for argparse to use with user generated input, accessed with args.user_prompt
	parser = argparse.ArgumentParser(description="Genai Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
	args = parser.parse_args()

	response = client.models.generate_content(
		model='gemini-2.5-flash', contents=args.user_prompt
    	)

	usage_metadata = response.usage_metadata
	if usage_metadata is None:
		raise RuntimeError("failed API request")

	prompt_tokens = usage_metadata.prompt_token_count
	response_tokens = usage_metadata.candidates_token_count

	
	
	print(f"Prompt tokens: {prompt_tokens}")
	print(f"Response tokens: {response_tokens}")
	
	
if __name__ == "__main__":
	main()
