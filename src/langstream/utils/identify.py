from nanoid import generate


def gen_thread_id():
    return f"thread_{generate()}"
