from skin_logic import extract_skin_signals, decide_next_step

vision_result = {
    "tags": [
        {"name": "skin", "confidence": 0.97},
        {"name": "face", "confidence": 0.99},
        {"name": "wall", "confidence": 0.90}
    ]
}

signals = extract_skin_signals(vision_result)
decision = decide_next_step(signals)

print("Skin signals:", signals)
print("Decision:", decision)

