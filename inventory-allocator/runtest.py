from src import InventoryAllocator
from os import walk, path
import json

testDir = "./test"

def run():
    tests = []
    for root, _, files in walk(testDir):
        tests.extend([path.join(root, name) for name in files])

    for test in tests:
        print("=========== running test: {} ===========".format(test))
        data = dict()

        with open(test) as f:
            data = json.load(f)

        print("json:\n{}\n".format(data))

        ia = InventoryAllocator()
        shipment = ia.process(data["order"], data["warehouse"]) 

        if shipment == data["shipment"]:
            print("=========== Passed! ===========");
        else:
            print("=========== Failed! ===========\nExpected: {}\nGot: {}\n".format(data["shipment"], shipment)); 

        input("press any key to continue...");

if __name__ == "__main__":
    run()
