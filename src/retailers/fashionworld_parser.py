from .base_parser import BaseParser

class FashionWorldParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        products = api_data.get("products", [])
        if not products: return {"search_term": search_keyword, "error": "No products returned."}
        
        llm_texts = []
        for i, product in enumerate(products):
            title = product.get('title', 'N/A').strip() or 'N/A'
            desc = product.get('description', 'N/A').strip() or 'N/A'
            material = product.get('material', 'N/A')
            variant = product.get('models', [{}])[0].get('variants', [{}])[0]
            color = variant.get('color', 'N/A')
            gender = variant.get('gender', 'N/A')
            llm_texts.append(f"""prod {i + 1}:
title: {title}
description: {desc}
material: {material}
gender: {gender}
color: {color}""")
        return self._format_llm_output(search_keyword, llm_texts)