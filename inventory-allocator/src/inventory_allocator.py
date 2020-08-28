# inventory_allocator.py
# Samuel Schmidt 2020-08-24

class InventoryAllocator():
    
    """ Originally made this entire class, but the task was updated halfway through
        so it's confined to a single function
    """
    def process(self, order: dict, warehouses: list) -> list:
        error = None
        shipment = []
        
        # using rectified sign to increase score only if the order amount is greater than the 
        # warehouse stock
        rectifiedSum = lambda oValue, wValue: \
             sum([max(o - w, 0) for (o,w) in zip(oValue, wValue)])

        # assign an index to each of the warehouses for score calculation.
        # if an ordered item is not listed in the inventory, give it 0
        for i in range(len(warehouses)):
            warehouses[i]['idx'] = i

            for item in order.keys():
                if warehouses[i]['inventory'].get(item) is None:
                    warehouses[i]['inventory'][item] = 0

        while len(order) > 0 and len(warehouses) > 0:
            # find the warehouse that is currently closest to completing our order
            best = min(warehouses, key=lambda w, o=order, s=rectifiedSum: 
                s(o.values(), w['inventory'].values()) + w['idx']
            )
            removeList = []
            warehouseOrder = {best['name']: dict()} 

            for item, amount in order.items():
                inventory = best['inventory'][item]

                if inventory != 0:

                    if amount <= inventory: # order is satisfied
                        warehouseOrder[best['name']][item] = amount
                        removeList.append(item)
                    else:
                        warehouseOrder[best['name']][item] = inventory
                        order[item] -= inventory

            for i in removeList: order.pop(i)

            if len(warehouseOrder[best['name']]) > 0: shipment.append(warehouseOrder)
            warehouses.remove(best)

        if len(order) != 0: return list()

        return shipment 
