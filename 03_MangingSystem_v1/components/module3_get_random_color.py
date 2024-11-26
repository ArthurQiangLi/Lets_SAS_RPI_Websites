import random

def extern_get_random_color():
    # Restrict RGB components to low values (0–100 for dark colors)
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(0, 100)
    return f"#{r:02x}{g:02x}{b:02x}"