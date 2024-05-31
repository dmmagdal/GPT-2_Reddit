# GPT-2_Reddit
Code here will train language models on text pulled from Reddit and post its own contributions to the site.


### gpt2-interactive.py

gpt2-interactive.py tests whether the huggingface transformers module (Tensorflow cpu version) can be run in
docker. To build the docker image, use the following command.

docker build -t gpt2-interactive-tfcpu -f docker-gpt-interactive-tfcpu .

To run the container and access the prompt, issue the following docker command into the console.

docker run -it huggingface-tfcpu


### huggingface docker images

These are additional docker images huggingface has published. These may come in handy later.

huggingface/transformers-cpu
huggingface/transformers-tensorflow-cpu
huggingface/transformers-tensorflow-gpu