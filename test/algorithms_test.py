from dsp_toolbox.optimization.binary_search import BinaryHalf, BinarySearch


def test_binary_search():
    bs = BinarySearch()
    bs.generate_data(1, 1000, 1000)
    
    target = 624
    val = bs.step(BinaryHalf.INIT)
    
    for _ in range(len(bs.data)):
        print(val)
        if val == target:
            return
        if val > target:
            val = bs.step(BinaryHalf.LOWER)
        if val < target:
            val = bs.step(BinaryHalf.UPPER)

def main():
    test_binary_search()


if __name__ == "__main__":
    main()