from src import InventoryAllocator
from os import walk, path
import json

testDir = "./test"

def run():
    tests = []
    for root, _, files in walk(testDir):
        tests.extend([path.join(root, name) for name in files])

    for test in tests:
        print("running test: {}".format(test))
        data = dict()

        with open(test) as f:
            data = json.load(f)

        print("json: {}\n".format(data))

        inventoryAllocator = InventoryAllocator(data["order"], data["warehouse"])
        inventoryAllocator.process() 

if __name__ == "__main__":
    run()
