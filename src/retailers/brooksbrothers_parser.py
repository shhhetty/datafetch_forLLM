from .base_parser import BaseParser

class BrooksBrothersParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        products = api_data.get("products", [])
        if not products: return {"search_term": search_keyword, "error": "No products returned."}
        
        llm_texts = []
        for i, product in enumerate(products):
            details = []
            def add(key, val):
                if val: details.append(f"{key}: {val}")
            
            add("title", product.get("title"))
            add("description", product.get("description"))
            add("gender", product.get("gender"))
            add("color", product.get("color"))
            
            attrs = product.get("cu_attributes", {})
            add("keyphrases", ", ".join(attrs.get("KEYPHRASE", [])))
            add("occasion", ", ".join(attrs.get("OCCASION", [])))
            add("material", ", ".join(attrs.get("FABRIC", [])) or product.get("material"))
            
            fit = product.get('models', [{}])[0].get('variants', [{}])[0].get("fit")
            add("fit", fit)

            if details:
                llm_texts.append(f"prod {i + 1}:\n" + "\n".join(details))
        return self._format_llm_output(search_keyword, llm_texts)