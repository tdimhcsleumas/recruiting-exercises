from src import InventoryAllocator
from os import walk, path
from sys import argv
import json

testDir = "./test"

def sameMembers(list_a: list, list_b: list) -> bool:
    for entry in list_a:
        if entry not in list_b:
            return False
    return True

def run(verbose=None):
    tests = []
    for root, _, files in walk(testDir):
        tests.extend([path.join(root, name) for name in files])

    for test in tests:
        data = dict()

        with open(test) as f:
            data = json.load(f)

        ia = InventoryAllocator()
        shipment = ia.process(data["order"], data["warehouse"]) 
        passed = sameMembers(shipment, data["shipment"])

        print("=========== Running test {} ===========".format(test))

        if verbose:
            print("json:\n{}\n".format(data))

            if passed:
                print("=========== Passed! ===========");
        
        if not passed:
            print("=========== Failed! ===========\nExpected: {}\nGot: {}\n".format(data["shipment"], shipment)); 


if __name__ == "__main__":
    option = argv[1] if len(argv) >= 2 else None
    run(verbose=option == 'verbose')
