# Duke MEng AIPI ChatBot

This is a chatbot that can answer questions about the Duke MEng AIPI program. Built using streamlit as the frontend and a Mistral-7B model fine tuned on [instruction data](https://huggingface.co/datasets/sail/symbolic-instruction-tuning/viewer/default/train)

## Dataset Collection

- Scraped the internal and external program websites for the Duke MEng AIPI program.
- Iterated over each link present in the `sitemap.xml` [file](https://ai.meng.duke.edu/sitemap.xml)
- Extracted the text from each link and saved it in a JSON file.
- Also copied over the FAQ doc from the internal program website
- Once I had a list of all these files, iterated over each file and passed the scraped data on to Gemini for further cleaning and better formatting
- Saved all the cleaned data in a single text file: `data/processed/context.txt`
<img width="330" alt="Screenshot 2024-04-18 at 11 15 32 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/455a359b-a896-4b71-a1b4-7fc83df9adeb">

## System Architecture

There are 3 primary components to the system
- Vector Database
- HuggingFace Inference Endpoint
- Streamlit Application

Workflow:
Once the `context.txt` file was created, chunked the document by paragraphs. Each paragraph was then converted to vector embeddings using the `all-MiniLM-L6-v2` model. These embeddings were then stored in `ChromaDB`. ChromaDB was hosted on Azure on compute optimized instance with the following specs:
<img width="1089" alt="Screenshot 2024-04-18 at 11 06 42 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/1f8e2ef2-9675-4f6a-a684-ba8fb4e13938">

The script for ingestion can be found in `scripts/ingest_data_into_vector_db.py`

The model is deployed on a dedicated HuggingFace serverless protected endpoint which can only be accessed using a certain `HF_TOKEN` which is injected into the streamlit app as an environment variable:
<img width="1265" alt="Screenshot 2024-04-18 at 11 17 48 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/85dad29a-22a7-4ddc-80d7-b90e8e9b18cf">

Finally this model API endpoint was called by the streamlit interface:
<img width="1326" alt="Screenshot 2024-04-18 at 11 55 23 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/a173d601-4beb-4717-a002-21226c4dffc9">

## Performance Evaluation

Using Human-as-a-Judge for the performance metric. 3 testers including myself evaluated the response of the model to the same 20 questions. On average, the model answered 16/20 questions correctly. Sample of questions used:
```
1. What courses does Professor Brinnae Bent take?
2. Who is the director of the AIPI program?
3. What are some housing options nearby?
4. How many credits do I need to graduate?
5. What courses can I take in the fall?
...
```

## Cost estimation
Training (RunPod): 2 GPU x 80GB VRAM H100 NVIDIA GPU + 125 GB RAM: $4.59 / hr
<img width="847" alt="Screenshot 2024-04-18 at 11 09 32 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/c9935800-4467-47ef-bb2c-38b6fb65a7b6">

Inference (HuggingFace Serverless Inference Endpoint - Dedicated): 1 GPU x 80GB VRAM A100 NVIDIA GPU + 145 GB RAM: $4 / hr
<img width="1248" alt="Screenshot 2024-04-18 at 11 11 39 AM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/b23744bc-c7ea-4b94-a65f-aaee8d589817">

Hosting ChromaDB (Azure): 1 Standard_F4s_v2 - $ 0.0169 / hr
<img width="1217" alt="Screenshot 2024-04-18 at 12 03 56 PM" src="https://github.com/rootsec1/duke-meng-ai-chatbot/assets/20264867/e5f70807-21dd-42df-b71c-2028bbb8a4aa">

## Approach to cost minimization
- Training: Quantize the model and use techniques like `QLora` for finetuning (this way we can train it on a massive CPU cluster instead of 1 big GPU but this would be slower)
- Inference: This was the cheapest option available, tried `RunPod` serverless and `HuggingFace`, even the smaller T4 GPUs don't work because it's a 7B model
- Hosting ChromaDB (Azure): Can use a smaller instance here with lesser vCPUs and RAM

  ## Demo

  Use [this link](https://duke-aipi-bot.streamlit.app/)
