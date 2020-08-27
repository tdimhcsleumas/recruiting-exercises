# inventory-allocator.py
# Samuel Schmidt 2020-08-24

class InventoryAllocator():

    def sumDifferences(warehouse: dict, order: dict):
        rect = lambda x, y: x - y if x > y else 0
        wValue = warehouse['inventory'].values()
        oValue = order.values()
        return sum([rect(o,w) for (w,o) in zip(wValue, oValue)])


    """ just a single function 
    """
    def process(self, order: dict, warehouses: list) -> list:
        error = None
        shipment = dict()

        # assign an index to each of the warehouses for score calculation.
        # if an ordered item is not listed in the inventory, give it 0
        for i in range(len(warehouses)):
            warehouses[i]['idx'] = i

            for item in order.keys():
                if warehouses[i]['inventory'].get(item) is None:
                    warehouses[i]['inventory'][item] = 0

        while len(order) > 0 and len(warehouses) > 0:
            # finding the warehouse that is currently closest to completing our order
            best = min(warehouses, key=lambda w, o=order, s=InventoryAllocator.sumDifferences: 
                s(w, o) + w['idx']
            )
            print(best)
            removeList = []

            for item, amount in order.items():
                inventory = best['inventory'][item]
                
                if inventory == 0:
                    continue

                if shipment.get(best['name']) is None:
                    shipment[best['name']] = dict()

                if amount <= inventory: # order is satisfied
                    shipment[best['name']][item] = amount
                    removeList.append(item)
                else:
                    shipment[best['name']][item] = inventory
                    order[item] -= inventory

            for i in removeList: order.pop(i)
            warehouses.remove(best)

        if len(order) != 0:
            return list()

        return [{k: v} for k, v in shipment.items()]
