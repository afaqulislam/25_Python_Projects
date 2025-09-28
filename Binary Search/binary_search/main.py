# main.py

from binary_search import binary_search_iterative, binary_search_recursive
from utils import generate_sorted_list


def main():
    print("🔍 Binary Search Demo")
    data = generate_sorted_list()
    print(f"\nSorted List:\n{data}")

    try:
        target = int(input("\nEnter the number to search: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    print("\nSearching using Iterative Method...")
    result_iter = binary_search_iterative(data, target)

    print("Searching using Recursive Method...")
    result_rec = binary_search_recursive(data, target, 0, len(data) - 1)

    if result_iter != -1:
        print(f"\n✅ Found at index {result_iter} (Iterative)")
    else:
        print("\n❌ Not found (Iterative)")

    if result_rec != -1:
        print(f"✅ Found at index {result_rec} (Recursive)")
    else:
        print("❌ Not found (Recursive)")


if __name__ == "__main__":
    main()
