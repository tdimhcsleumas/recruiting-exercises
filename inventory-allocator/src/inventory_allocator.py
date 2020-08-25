# inventory-allocator.py
# Samuel Schmidt 2020-08-24

class InventoryItem(dict):
    
    kTotal = "total"
    kWarehouse = "warehouse"

    def __init__(self):
        self[self.kTotal] = 0
        self[self.kWarehouse] = dict()


    def addWarehouse(self, name: str, quantity: int):
        self[self.kTotal] += quantity
        self[self.kWarehouse][name] = quantity

class InventoryAllocator():
    
    def __init__(self, order: dict, warehouses: list):
        self.order = order
        self.warehouses = warehouses
        self.items = dict()

    def generateItems(self):
        for warehouse in self.warehouses:
            name = warehouse.get("name")

            for (item, quantity) in warehouse.get("inventory").items():
                if self.items.get(item) is None:
                    self.items[item] = InventoryItem()
                
                self.items.get(item).addWarehouse(name, quantity)
        
    def getItems(self) -> dict:
        return self.items

    def process(self) -> list:
        return list() 
