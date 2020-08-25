# inventory-allocator.py
# Samuel Schmidt 2020-08-24

""" helper class to make querying items more convenient
    these items will be store in a dictionary, keyed in by name
    ex:
    "chicken" : {
        "total": 10,
        "warehouse: {
            "od": 8,
            "om": 2
        }
    }

"""
class InventoryItem(dict):
    
    kTotal = "total"
    kWarehouse = "warehouse"

    def __init__(self):
        self["total"] = 0
        self["warehouse"] = dict()

    """ increment the total number of this item. generate the name, quantity pair
        for the specified warehouse
    """
    def addWarehouse(self, name: str, quantity: int):
        self["total"] += quantity
        self["warehouse"][name] = quantity

    def getTotal(self) -> int:
        return self.get("total")

    def getWarehouses(self) -> dict:
        return self.get("warehouse")

""" helper class to make generating the required list more convenient
"""
class WarehouseOrder(dict):
    """ insert item, amount order into specified warehouse. create dict if None
    """
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
        self.items = dict()

    """ fill in item dictionary to survey the total number of items as well
        as which warehouses have them.
    """
    def generateItems(self):
        for warehouse in self.warehouses:
            name = warehouse.get("name")

            for (item, quantity) in warehouse.get("inventory").items():
                if self.items.get(item) is None:
                    self.items[item] = InventoryItem()
                
                self.items.get(item).addWarehouse(name, quantity)
        
    """ After the dictionary of items is generated, surveying the complete stock,
        process the orders. Store the order for each warehouse as a dictionary 
        keyed in by name so that updates are efficient. Export as a list upon return.
    """
    def process(self) -> list:
        error = None
        shipment = WarehouseOrder()

        for item, quantity in self.order.items():
            if self.items.get(item) is None or self.items.get(item).getTotal() < quantity:
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
