thonimport json

def load_input(filename='data/inputs.txt'):
    with open(filename, 'r') as file:
        return file.read().strip()

def save_output(data, filename='data/outputs.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")