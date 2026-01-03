from recommendations import recommend_products

budget = "medium"
products = recommend_products(budget)

print(f"Recommended {budget} products:")
for p in products:
    print("-", p)

