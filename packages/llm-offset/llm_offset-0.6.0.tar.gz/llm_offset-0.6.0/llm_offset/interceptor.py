def llm_offset_decorator(email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Sending notification to {email}")
            return result
        return wrapper
    return decorator

def log_call(openai, email):
    original_text = openai.chat.completions.create
    openai.chat.completions.create = llm_offset_decorator(email)(original_text)

    original_image = openai.image.generate
    openai.image.generate = llm_offset_decorator(email)(original_image)