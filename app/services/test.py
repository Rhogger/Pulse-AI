import os
from pathlib import Path


root_dir = Path(__file__).parent.parent.parent
credentials_path = os.path.join(root_dir, 'credentials.json')

print(root_dir)
print(credentials_path)
