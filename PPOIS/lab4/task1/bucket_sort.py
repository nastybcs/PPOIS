from task1.selection_sort import SelectionSort
class BucketSort: 
    def bucket_sort (data, key=None, bucket_counts = 10):
        arr = list(data)
        if len(arr) <= 1:
            return arr
        key = key or (lambda x:x)
        values = [key(x) for x in arr]
        mn , mx = min(values), max(values)
        if mn == mx:
            return arr
        interval = (mx - mn) / bucket_counts
        buckets = [[] for i in range(bucket_counts)]

        for item in arr:
            index = int((key(item) - mn) / interval)
            if index == bucket_counts:
                index -=1
            buckets[index].append(item)
        result = []
        for bucket in buckets:
           if bucket:
                result.extend(SelectionSort.selection_sort(bucket, key))
        return result