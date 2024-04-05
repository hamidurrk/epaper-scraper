from datetime import datetime

def timestamp_to_datetime(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)  
    return dt_object

# # Example usage:
# timestamp = 1364839199999  # Replace this with your timestamp
# dt = timestamp_to_datetime(timestamp)
# print("Human-readable date and time:", dt)

# timestamp = 1364752800000  # Replace this with your timestamp
# dt = timestamp_to_datetime(timestamp)
# print("Human-readable date and time:", dt)

def date_to_timestamp(input_date):
    min_combined_datetime = datetime.combine(input_date, datetime.min.time())
    max_combined_datetime = datetime.combine(input_date, datetime.max.time())

    min_timestamp = int(min_combined_datetime.timestamp() * 1000)  
    max_timestamp = int(max_combined_datetime.timestamp() * 1000)  
    return min_timestamp, max_timestamp

input_date = datetime(2013, 4, 1)  
min, max = date_to_timestamp(input_date)
print("Unix timestamp:", min, max)
