# inventory-allocator.py
# Samuel Schmidt 2020-08-24

class InventoryAllocator():

    """ just a single function 
    """
    def process(self, order: dict, warehouses: list) -> list:
        error = None
        shipment = dict()
        rectifier = lambda x, y: x - y if x > y else 0

        # assign an index to each of the warehouses for score calculation.
        # if an ordered item is not listed in the inventory, give it 0
        for i in range(len(warehouses)):
            warehouses[i]['idx'] = i

            for item in order.keys():
                if warehouses[i]['inventory'].get(item) is None:
                    warehouses[i]['inventory'][item] = 0

        for item, quantity in order.items(): 
            wCopy = warehouses.copy()

            while quantity > 0 and len(wCopy) > 0: 
                # find lowest score where being close to the desired quantity
                # is favored if less than the desired, and index is favored since 
                # it represents how expensive it is. recalculate this ever iteration 
                # since the desired quantity decreases over time in order to complete
                # the order
                best = min(wCopy, key=lambda w, i=item, q=quantity, r=rectifier: 
                    r(q, w['inventory'][i]) + w['idx']
                )
                inventory = best['inventory'][item]
                decrement = quantity if quantity < inventory else inventory

                if shipment.get(best['name']) is None:
                    shipment[best['name']] = dict()

                shipment[best['name']][item] = decrement 
                quantity -= decrement
                wCopy.remove(best)


            if quantity > 0:
                error = "could not fulfill order for {}".format(item)
                break

        if error is not None:
            print(error)
            return list()

        return [{k: v} for k, v in shipment.items()]
