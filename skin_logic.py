def extract_skin_signals(vision_result):
    tags = vision_result.get("tags", [])
    
    skin_related = []
    for tag in tags:
        name = tag["name"].lower()
        confidence = tag["confidence"]

        if name in [
            "skin", "face", "cheek", "forehead",
            "chin", "jaw", "neck"
        ] and confidence > 0.85:
            skin_related.append(name)

    return list(set(skin_related))


def decide_next_step(skin_signals):
    if not skin_signals:
        return {
            "action": "ask_image_again",
            "message": "We couldn’t clearly analyze your skin. Please upload a clearer image in good lighting."
        }

    return {
        "action": "ask_questions",
        "questions": [
            "What is your age?",
            "How would you describe your skin type? (oily, dry, combination, sensitive)",
            "What is your main concern? (acne, pigmentation, irritation, texture)",
            "What is your budget range? (low / medium / premium)"
        ]
    }

