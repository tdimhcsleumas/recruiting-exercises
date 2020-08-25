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

    def getTotal(self):
        return self.get(self.kTotal)

    def getWarehouses(self):
        return self.get(self.kWarehouse)

class WarehouseOrder(dict):
    def addOrder(self, warehouse: str, item: str, amount: int):
        if self.get(warehouse) is None:
            self[warehouse] = dict()
        self[warehouse][item] = amount
        
    def toList(self) -> list:
        return [{k: v} for k, v in self.items()]

class InventoryAllocator():
    
    def __init__(self, order: dict, warehouses: list):
        self.order = order
        self.warehouses = warehouses
        self.warehouseOrders = WarehouseOrder()
        self.items = dict()

    def generateItems(self):
        for warehouse in self.warehouses:
            name = warehouse.get("name")

            for (item, quantity) in warehouse.get("inventory").items():
                if self.items.get(item) is None:
                    self.items[item] = InventoryItem()
                
                self.items.get(item).addWarehouse(name, quantity)
        
    def process(self) -> list:
        error = None
        shipment = WarehouseOrder()

        for item, quantity in self.order.items():
            if self.items.get(item).getTotal() < quantity:
                error = "not enough stock for {}".format(item)
                break;
            
            for warehouse, inventory in self.items.get(item).getWarehouses().items():
                if quantity <= 0:
                    break
                elif quantity <= inventory:
                    shipment.addOrder(warehouse, item, quantity)
                    quantity -= quantity
                else:
                    shipment.addOrder(warehouse, item, inventory)
                    quantity -= inventory

        if error is not None:
            print(error)
            return list()

        return shipment.toList()
