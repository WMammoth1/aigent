import os
from dotenv import load_dotenv
from google import genai

def main():
    
	load_dotenv()
	api_key = os.environ.get('GEMINI_API_KEY')

	if api_key == None:
		raise RuntimeError("environmental variable was not found")

	client = genai.Client(api_key=api_key)

	print("Hello from aigent!")

	response = client.models.generate_content(
		model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
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
