from .base_parser import BaseParser

class DillardsParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        products = api_data.get("products", [])
        if not products: return {"search_term": search_keyword, "error": "No products returned."}
        
        extracted_products = []
        for product in products:
            extracted_products.append({
                "title": product.get("title", "N/A"),
                "description": product.get("description", "N/A"),
                "gender": product.get("gender", "N/A"),
                "age": product.get("age", "N/A"),
                "color": product.get("color", "N/A"),
                "material": product.get("material", "N/A"),
                "topologies": product.get("topologies", []),
                "sleeve_length": product.get("sleeve_length", []),
                "occasion": product.get("occasion", []),
                "fabric_type": product.get("fabric_type", []),
            })
        return {"search_term": search_keyword, "products": extracted_products}