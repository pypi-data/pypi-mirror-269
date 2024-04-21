import requests


def llm_offset_decorator_for_text(email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                requests.post(
                    'https://calltochange.vercel.app/api/text?email=' + email)
            except requests.RequestException as e:
                print(f"Failed to send text offset: {e}")
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator


def llm_offset_decorator_for_image(email):
    def decorator(func):
        def wrapper(*args, **kwargs):

            try:
                requests.post(
                    'https://calltochange.vercel.app/api/image?email=' + email)
            except requests.RequestException as e:
                print(f"Failed to send image offset: {e}")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def log(openai_client, email):
    original_text = openai_client.chat.completions.create
    openai_client.chat.completions.create = llm_offset_decorator_for_text(
        email)(original_text)

    original_image = openai_client.images.generate
    openai_client.images.generate = llm_offset_decorator_for_image(
        email)(original_image)
