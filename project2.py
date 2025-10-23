import csv
from haversine import *
import random  # Added for random pivot selection

# Store class represents a store location with all relevant attributes
class Store:
    def __init__(self, store_id, address, city, state, zip_code, latitude, longitude):
        self.store_id = int(store_id)  # Ensure store_id is stored as integer
        self.address = str(address)    # Ensure address is stored as string
        self.city = str(city)          # Ensure city is stored as string
        self.state = str(state)        # Ensure state is stored as string
        self.zip_code = str(zip_code)  # Ensure zip_code is stored as integer
        self.latitude = float(latitude)  # Ensure latitude is stored as float
        self.longitude = float(longitude)  # Ensure longitude is stored as float

    def __repr__(self):
        # String representation for debugging
        return f"Store({self.store_id}, {self.address}, {self.city}, {self.state}, {self.zip_code}, {self.latitude}, {self.longitude})"
    
# Query class represents a user's query for nearest stores
class Query:
    def __init__(self, latitude, longitude, num_stores_desired):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.num_stores_desired = int(num_stores_desired)
        self.starbucks_distances = []      # List of dicts: {'store': Store, 'distance': float}
        self.whataburger_distances = []    # List of dicts: {'store': Store, 'distance': float}

    def __repr__(self):
        # String representation for debugging
        return f"Query({self.latitude}, {self.longitude}, {self.num_stores_desired})"

# Loads store location data from a CSV file and returns a list of Store objects
def load_location_data(file_path):
    stores = []
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            store = Store(
                store_id=row['Store ID'],
                address=row['Address'],
                city=row['City'],
                state=row['State'],
                zip_code=row['Zip Code'],
                latitude=row['Latitude'],
                longitude=row['Longitude']
            )
            stores.append(store)
    return stores

# Loads query data from a CSV file and returns a list of Query objects
def load_query_data(file_path):
    queries = []
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = Query(
                latitude=row['Latitude'],
                longitude=row['Longitude'],
                num_stores_desired=row['Number of stores desired']
            )
            queries.append(query)
    return queries

# Lomuto partition scheme with random pivot for array of dicts using 'distance' as key.
def Partition(A, l, r):
    pivot_index = random.randint(l, r)
    A[pivot_index], A[r] = A[r], A[pivot_index]  # Move pivot to end
    pivot = A[r]['distance']
    i = l - 1
    for j in range(l, r):
        if A[j]['distance'] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1

# Randomized selection algorithm to find the i-th smallest element in array of dicts using 'distance' as key.
def RandSelect(A, l, r, i):
    if l == r:
        return A[l]
    
    pivot_index = Partition(A, l, r)
    
    k = pivot_index - l
    
    if i == k:
        return A[pivot_index]
    elif i < k:
        return RandSelect(A, l, pivot_index - 1, i)
    else:
        return RandSelect(A, pivot_index + 1, r, i - (k + 1))

# In-place quicksort for sorting array of dicts by 'distance' key
def QuickSort(A, l, r):
    if l < r:
        pivotIndex = Partition(A, l, r)
        QuickSort(A, l, pivotIndex - 1)
        QuickSort(A, pivotIndex + 1, r)

# Main function to load data, process queries, and print results
def main():
    # Load queries from file
    queries = load_query_data("Queries.csv")

    # Load Starbucks and Whataburger store data
    starbucks_stores = load_location_data("StarbucksData.csv")
    whataburger_stores = load_location_data("WhataburgerData.csv")

    # For each query, compute and store distances to all Starbucks and Whataburger stores
    for query in queries:
        for store in starbucks_stores:
            distance = haversine(query.latitude, query.longitude, store.latitude, store.longitude)
            query.starbucks_distances.append({'store': store, 'distance': distance})
        for store in whataburger_stores:
            distance = haversine(query.latitude, query.longitude, store.latitude, store.longitude)
            query.whataburger_distances.append({'store': store, 'distance': distance})

    # For each query, find and print the closest Starbucks stores
    for query in queries:
        i = query.num_stores_desired - 1
        n = len(query.starbucks_distances)
        if n > i:
            # Use RandSelect to partition the closest i+1 stores, then sort them
            RandSelect(query.starbucks_distances, 0, n - 1, i)
            QuickSort(query.starbucks_distances, 0, i)
            print(f"The {i+1} closest STARBUCKS stores to ({query.latitude}, {query.longitude}):")
            for entry in query.starbucks_distances[:i+1]:
                store = entry['store']
                print(f"Store #{store.store_id}. {store.address}, {store.city}, {store.state}, {store.zip_code}. - {entry['distance']:.2f} miles.")
            print()
    # For each query, find and print the closest Whataburger stores
    for query in queries:
        i = query.num_stores_desired - 1
        n = len(query.whataburger_distances)
        if n > i:
            # Use RandSelect to partition the closest i+1 stores, then sort them
            RandSelect(query.whataburger_distances, 0, n - 1, i)
            QuickSort(query.whataburger_distances, 0, i)
            print(f"The {i+1} closest WHATABURGER stores to ({query.latitude}, {query.longitude}):")
            for entry in query.whataburger_distances[:i+1]:
                store = entry['store']
                print(f"Store #{store.store_id}. {store.address}, {store.city}, {store.state}, {store.zip_code}. - {entry['distance']:.2f} miles.")
            print()

# Entry point for the script
if __name__ == "__main__":
    main()
