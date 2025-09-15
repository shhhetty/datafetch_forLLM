from .base_parser import BaseParser

class SimplyBeParser(BaseParser):
    def parse_response(self, search_keyword, api_data):
        products = api_data.get("products", [])
        if not products: return {"search_term": search_keyword, "error": "No products returned."}

        llm_texts = []
        for i, product in enumerate(products):
            details = []
            
            def add_detail(field_name, value):
                if not value: return
                val_str = ", ".join(map(str, value)) if isinstance(value, list) else str(value)
                if val_str.strip():
                    details.append(f"{field_name}: {val_str}")

            add_detail("google_product_category", product.get("google_product_category"))
            add_detail("description", product.get("description"))
            add_detail("title", product.get("title"))
            add_detail("product_type", product.get("product_type"))
            add_detail("FABRIC", product.get("material")) # Aliasing

            extra = product.get("extra_attributes", {})
            cu = product.get("cu_attributes", {})
            add_detail("SEASON", extra.get("SEASON") or cu.get("SEASON"))
            add_detail("OCCASION", extra.get("OCCASION") or cu.get("OCCASION"))
            add_detail("VIBE", extra.get("VIBE"))
            add_detail("LOOK", extra.get("LOOK"))
            
            if details:
                llm_texts.append(f"prod {i + 1}:\n" + "\n".join(details))
        return self._format_llm_output(search_keyword, llm_texts)