# Sample skincare products by budget tier

PRODUCTS = {
    "Dot & Key": {
        "low": [
            "Dot & Key Glow Moisturizer - ₹350",
            "Dot & Key Hydrating Face Wash - ₹299"
        ],
        "medium": [
            "Dot & Key Vitamin C Serum - ₹699",
            "Dot & Key Retinol Night Cream - ₹899"
        ],
        "premium": [
            "Dot & Key Complete Skincare Kit - ₹2999"
        ]
    },
    "Minimalist": {
        "low": [
            "Minimalist 2% Hyaluronic Acid Serum - ₹399",
            "Minimalist Vitamin C Face Wash - ₹299"
        ],
        "medium": [
            "Minimalist 10% Niacinamide + Zinc Serum - ₹699",
            "Minimalist Sunscreen SPF 50 - ₹499"
        ],
        "premium": [
            "Minimalist Complete Skincare Set - ₹2599"
        ]
    },
    "Derma Co": {
        "low": [
            "Derma Co Face Wash - ₹299"
        ],
        "medium": [
            "Derma Co Vitamin C Serum - ₹799",
            "Derma Co Sunscreen SPF 50 - ₹499"
        ],
        "premium": [
            "Derma Co Anti-Acne Kit - ₹2999"
        ]
    }
}

def recommend_products(budget):
    budget = budget.lower()
    recommendations = []

    for brand, tiers in PRODUCTS.items():
        if budget in tiers:
            recommendations.extend(tiers[budget])
    
    return recommendations if recommendations else ["No products found for this budget"]


