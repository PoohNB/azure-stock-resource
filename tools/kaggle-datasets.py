import kagglehub

# Download latest version
path = kagglehub.dataset_download("gpreda/bbc-news")

print("Path to dataset files:", path)