import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

url = "https://en.wikipedia.org/wiki/Software_metric"
cycles = 10

# Initialize the Chrome browser with the WebDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_performance_data():
    # Open the URL
    driver.get(url)

    # Execute the JavaScript to get performance metrics
    performance_script = 'return window.performance.getEntries();'
    performance_data = driver.execute_script(performance_script)

    return performance_data


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def extract_data_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'duration'])

        for entry in data:
            name = entry.get('name', '')
            duration = entry.get('duration', 0)
            writer.writerow([name, duration])


# Perform the measurements in a loop
total_performance_data = []

for _ in range(cycles):
    performance_data = get_performance_data()
    total_performance_data.extend(performance_data)
    time.sleep(2)  # Add a delay between cycles

# Calculate the average performance
average_performance = sum(entry.get('duration', 0) for entry in total_performance_data) / len(total_performance_data)

# Write raw JSON data to a file
write_json_to_file(total_performance_data, 'performance_data.json')

# Write extracted data to a CSV file
extract_data_to_csv(total_performance_data, 'performance_data.csv')

# Print average performance
print(f"Average Performance: {average_performance} milliseconds")

# Close the browser window
driver.quit()
