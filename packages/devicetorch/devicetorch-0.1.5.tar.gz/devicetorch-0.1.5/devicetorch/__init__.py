def get(torch):
  if torch.backends.mps.is_available():
    return "mps"
  elif torch.cuda.is_available():
    return "cuda"
  else:
    return "cpu"
def empty_cache(torch):
  if torch.backends.mps.is_available():
    torch.mps.empty_cache()
  elif torch.cuda.is_available():
    torch.cuda.empty_cache()
