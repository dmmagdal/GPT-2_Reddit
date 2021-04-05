# gpt2-interactive.py
# author: Diego Magdaleno
# Create an interactive program in docker that uses GPT-2 huggingface.


from transformers import TFGPT2LMHeadModel, GPT2Tokenizer, TFGPT2Model



def main():
	# Initialize a tokenizer and model.
	tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
	model = TFGPT2LMHeadModel.from_pretrained("gpt2", from_pt=True)

	# Infinite loop.
	while True:
	#i = 0
	#while i == 0:
		# Take in the user input. If the input matches a certain
		# string, break out of the loop and exit the program.
		user_input = input("prompt:> ")
		if user_input == "<|endoftext|>":
			break
		#user_input = "And to the darkness, I cast a bright light. The shadow disolves "

		# Tokenize/encode the input text.
		#encoded_input = tokenizer.tokenize(user_input)
		encoded_input = tokenizer.encode(user_input, return_tensors="tf")

		# Generate samples.
		generated_samples = model.generate(encoded_input, 
											max_length=150,
											num_return_sequences=10,
											no_repeat_ngram_size=2,
											repetition_penalty=1.5,
											top_p=0.92,
											temperature=0.85,
											do_sample=True,
											top_k=125,
											early_stopping=True)

		# Print samples
		for i, beam in enumerate(generated_samples):
			print("{}: {}".format(i, tokenizer.decode(beam, skip_special_tokens=True)))
			print()
		#i += 1

	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()