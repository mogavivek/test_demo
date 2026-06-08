from typing import List

class ShoppingCart:
    def __init__(self, max_size:int):
        self.items:List[str] = []
        self.max_size = max_size
    
    def add_item(self, item:str):
        if self.item_size == self.max_size:
            raise OverflowError("Cannot add more items")
        self.items.append(item)
    
    def clear_all_item(self):
        self.items.clear()
    
    def item_size(self):
        return len(self.items)
    
    def get_items(self) -> List[str]:
        return self.items
    
    def get_total_price(self, price_map):
        total_price = 0
        for item in price_map:
            total_price = total_price + price_map.get(item)
        return total_price


class TestMath():
    def take_two_numbers()-> List[int]:
        a = 10
        b = 10
        return a,b