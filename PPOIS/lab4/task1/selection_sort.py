class SelectionSort:

    def selection_sort(arr, key= None):
        arr = arr[:]
        n = len(arr)
        key = key or (lambda x: x)
        for i in range(n):
            min_index = i 
            for j in range(i+1, n):
                if key(arr[j]) < key(arr[min_index]):
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
        return arr
