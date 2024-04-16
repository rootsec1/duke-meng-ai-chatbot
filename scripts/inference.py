from transformers import AutoModelForCausalLM, AutoTokenizer

import torch
import time


def get_ai_device() -> str:
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        return mps_device
    return "cuda" if torch.cuda.is_available() else "cpu"


DEVICE = get_ai_device()
print(f"Using device: {DEVICE}")


def setup_model(model_path: str) -> tuple:
    start_time = time.time()
    model = AutoModelForCausalLM.from_pretrained(model_path)
    print(f"Model loading time: {time.time() - start_time} seconds")

    start_time = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print(f"Tokenizer loading time: {time.time() - start_time} seconds")

    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

    start_time = time.time()
    model.to(DEVICE)
    print(f"Model transfer to device time: {time.time() - start_time} seconds")

    return model, tokenizer


def perform_inference_on_fine_tuned_model(prompt: str, model, tokenizer) -> str:
    start_time = time.time()
    inputs = tokenizer.encode(
        prompt + tokenizer.eos_token,
        return_tensors="pt"
    )
    print(f"Encoding time: {time.time() - start_time} seconds")

    inputs = inputs.to(DEVICE)

    start_time = time.time()
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=512,
            num_return_sequences=1
        )
    print(
        f"Model response generation time: {time.time() - start_time} seconds"
    )

    start_time = time.time()
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Decoding time: {time.time() - start_time} seconds")

    return response.strip()


if __name__ == "__main__":
    model, tokenizer = setup_model("./models/gemma-instruction-tuned")
    print("[INFERENCE] Model loaded successfully")
    fine_tuned_model_response = perform_inference_on_fine_tuned_model(
        prompt="How to make pasta?",
        model=model,
        tokenizer=tokenizer
    )
    print(fine_tuned_model_response)
