# inventory-allocator.py
# Samuel Schmidt 2020-08-24

""" helper class to make generating the required list more convenient
    just a dict wrapper, but i want to condense initialization
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
        
    """ Store the order for each warehouse as a dictionary 
        keyed in by name so that updates are efficient. Export as a list upon return.
    """
    def process(self) -> list:
        error = None
        shipment = WarehouseOrder()

        for item, quantity in self.order.items():

            for warehouse in self.warehouses:

                name = warehouse.get("name") 
                inventory = warehouse.get("inventory").get(item)

                if inventory is not None:
                    if quantity <= 0:
                        break
                    elif quantity <= inventory:
                        shipment.addOrder(name, item, quantity)
                        quantity -= quantity
                    else:
                        shipment.addOrder(name, item, inventory)
                        quantity -= inventory
            
            if quantity > 0:
                error = "not enough inventory for {}".format(item)
                break

        if error is not None:
            print(error)
            return list()

        return shipment.toList()
