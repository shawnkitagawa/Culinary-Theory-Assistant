STRICTNESS_CONFIG = {
    "strict": {
        "temperature": 0.1,
        "max_distance": 0.42,
        "instruction": (
            "Answer only with facts that are directly stated in the provided context. "
            "Do not add outside knowledge, examples, assumptions, or creative suggestions. "
            "If the context does not clearly answer the question, say: "
            "'I don't know based on the provided material.' "
            "Keep the answer concise. "
            "When possible, cite the exact source label and page range from the context."
        ),
    },
    "balanced": {
        "temperature": 0.3,
        "max_distance": 0.55,
        "instruction": (
            "Answer using the provided context as the source of truth. "
            "Explain the culinary theory, principles, causes, effects, and practical meaning. "
            "If the context partially answers the question, clearly say what is supported and what is not directly covered. "
            "You may give practical advice only when it logically follows from the retrieved context. "
            "Do not invent specific ingredients, recipes, or techniques that are not supported by the context. "
            "Use simple, clear English."
        ),
    },
    "creative": {
        "temperature": 0.55,
        "max_distance": 0.70,
        "instruction": (
            "Use the provided context as the foundation. "
            "If the context contains relevant culinary principles, mechanisms, techniques, or examples, do not stop at 'I don't know.' "
            "First explain what the sources directly support. "
            "Then add a clearly labeled section called 'Theory-based application' for reasonable extensions. "
            "The theory-based application must be connected to the retrieved context. "
            "Do not pretend creative applications are directly stated in the source. "
            "When suggesting ingredients or techniques, prefer examples from the context. "
            "If the exact ingredient is not in the context, speak in categories and principles rather than making unsupported source claims. "
            "Focus on useful culinary reasoning, tradeoffs, and practical implications."
        ),
    },
    "recipe": {
        "temperature": 0.65,
        "max_distance": 0.75,
        "instruction": (
            "Generate a helpful recipe-style recommendation using the retrieved context as the culinary foundation. "
            "Recipe mode should be practical and useful, not overly defensive. "
            "If the retrieved context does not mention the user's exact ingredient, but it contains related culinary theory, similar ingredients, "
            "fruit preparations, dairy principles, freezing principles, sugar balance, texture control, flavor balance, or technique examples, "
            "use those principles to make a careful recommendation. "
            "Clearly separate direct source support from creative application. "
            "Use these sections when appropriate: "
            "'Short answer', 'Supported by the sources', 'Creative recipe application', 'Basic method', and 'Why it works'. "
            "You may suggest reasonable spice combinations, flavor pairings, ingredient amounts, and methods as creative applications. "
            "Do not claim those suggestions are directly from the sources unless the context directly states them. "
            "If the exact topic is not directly covered, say: 'The sources do not directly mention this exact combination, but they provide related principles.' "
            "Only say 'I don't know based on the provided material' if the retrieved context is completely unrelated to the user's question."
        ),
    },
}


def get_strict_config(strictness_level: str) -> dict:
    return STRICTNESS_CONFIG[strictness_level]