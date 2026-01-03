def generate_response(step, data=None):
    if step == "welcome":
        return "Hi! I’m Eira 🌿 Upload a clear photo of your skin, and I’ll help you choose the right skincare."

    if step == "ask_questions":
        return (
            "Thanks! To help you better, I need a few details:\n"
            "1️⃣ Your age\n"
            "2️⃣ Skin type (oily, dry, combination, sensitive)\n"
            "3️⃣ Main concern (acne, pigmentation, irritation)\n"
            "4️⃣ Budget (low / medium / premium)"
        )

    if step == "recommend":
        products = data.get("products", [])
        response = "Based on your inputs, here are some product suggestions:\n\n"
        for p in products:
            response += f"• {p}\n"
        response += "\n⚠️ If irritation persists, please consult a dermatologist."
        return response

    return "I’m here to help! 😊"

