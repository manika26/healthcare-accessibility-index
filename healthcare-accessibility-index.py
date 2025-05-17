import os

folders = [
    "data/raw", "data/cleaned",
    "notebooks", "src", "app"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Folders created!")
