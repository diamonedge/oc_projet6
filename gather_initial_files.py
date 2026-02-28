import kagglehub, os

# Download latest version
os.environ["KAGGLEHUB_CACHE"]="./"

path = kagglehub.dataset_download("prasad22/healthcare-dataset")

print("Path to dataset files:", path)
