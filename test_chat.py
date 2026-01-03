from chat_flow import generate_response

print(generate_response("welcome"))
print()
print(generate_response("ask_questions"))
print()
print(generate_response("recommend", {
    "products": [
        "Minimalist Sunscreen SPF 50",
        "Dot & Key Vitamin C Serum"
    ]
}))

