from transformers import AutoModelForCausalLM, AutoTokenizer

import torch


def get_ai_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


DEVICE = get_ai_device()
print(f"Using device: {DEVICE}")


def setup_model(model_path: str) -> tuple:
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Set pad token to eos token (needed if it's not already set in the saved model/tokenizer)
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id
    model.to(DEVICE)

    return model, tokenizer


def perform_inference_on_fine_tuned_model(prompt: str, model, tokenizer) -> str:
    print("[INFERENCE] Encoding prompt...")
    inputs = tokenizer.encode(
        prompt + tokenizer.eos_token,
        return_tensors="pt"
    )
    inputs = inputs.to(DEVICE)  # Move to GPU if available

    print("[INFERENCE] Generating response from model...")
    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=512,
            num_return_sequences=1
        )

    print("[INFERENCE] Decoding response...")
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
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
