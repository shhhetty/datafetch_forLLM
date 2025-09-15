from .base_parser import BaseParser

class JcrewParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        products = api_data.get("products", [])
        if not products: return {"search_term": search_keyword, "error": "No products returned."}
        
        llm_texts = []
        LILY_KEYS = self.config['parser_settings']['lily_keys_to_extract']
        
        for i, product in enumerate(products):
            title = product.get('title', 'N/A')
            desc = product.get('description', 'N/A')
            topologies = ", ".join(product.get('topologies', [])) or 'N/A'
            
            variant = product.get('models', [{}])[0].get('variants', [{}])[0]
            gender = variant.get('gender', 'N/A')
            color = variant.get('color', 'N/A')
            
            lines = [f"prod {i + 1}:", f"title: {title}", f"description: {desc}", 
                     f"topologies: {topologies}", f"gender: {gender}", f"color: {color}"]

            for key in LILY_KEYS:
                if values := variant.get(key):
                    display_key = key.replace('lily_', '').replace('_', ' ')
                    lines.append(f"{display_key}: {', '.join(values)}")
            
            llm_texts.append("\n".join(lines))
        return self._format_llm_output(search_keyword, llm_texts)