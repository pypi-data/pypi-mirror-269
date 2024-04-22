import random
import importlib
import re

def check_for_random_numbers(source_code):
  """Checks whether the given source code contains random numbers.

  Args:
    source_code: The source code to check.

  Returns:
    True if the source code contains random numbers, False otherwise.
  """

  for line in source_code.splitlines():
    match = re.search(r"import\s+([a-zA-Z0-9_.]+)(?:\s+as\s+([a-zA-Z0-9_]+))?\s*", line)
    if match:
      library = match.group(1)
      alias = match.group(2) or library
      try:
        for m in importlib.import_module(library).__dict__.keys():
          if hasattr(getattr(importlib.import_module(library), m), "seed"):
            return True
      except ModuleNotFoundError:
        pass
  return False

def initialize_seeds(source_code):
  """Initializes all seeds for all API libraries in the source code file.

  Args:
    source_code: The source code to initialize seeds for.

  Returns:
    A new code with all seeds initialized.
  """
  new_code = ""
  aliases = {}
  for line in source_code.splitlines():
    match = re.search(r"import\s+([a-zA-Z0-9_.]+)(?:\s+as\s+([a-zA-Z0-9_]+))?\s*", line)
    if match:
      library = match.group(1)
      alias = match.group(2) or library
      aliases[alias] = library
      try:
        module = importlib.import_module(library)
        for m in module.__dict__.keys():
          if m=='experimental': tff1=1
          if hasattr(getattr(module, m), "seed"):
            if library == "gym":
              new_code += f"env.reset(seed=0)\n"
              new_code += f"env.action_space.seed(0)\n"
            elif library == "gymnasium":
              new_code += f"env.reset(seed=0)\n"
              new_code += f"env.action_space.seed(0)\n"
            elif library == "torch":
              t = "use_deterministic_algorithms"
              new_code += f"{alias}.{t}(True)\n"
              t = "manual_seed"
              new_code += f"{alias}.{t}(0)\n"
              if m == "Generator":
                new_code += f"{alias}.{m}().manual_seed(0)\n"
              elif m == "manual_seed":
                new_code += f"{alias}.{m}(0)\n"
              elif m == "initial_seed":
                new_code += f"{alias}.{m}()\n"
              elif m == "cuda":
                new_code += f"{alias}.{m}.manual_seed(0)\n"
                new_code += f"{alias}.{m}.manual_seed_all(0)\n"
            elif library == "tensorflow":
              new_code += f"{alias}.random.set_seed(0)\n"
              if tff1==1: 
                new_code += f"{alias}.experimental.numpy.random.seed(0)\n"
                new_code += f"{alias}.keras.utils.set_random_seed(0)\n"
            elif library == "pylab":
              new_code += f"{alias}.seed(0)\n"
            elif library == "random":
              if m == "Random":
                new_code += f"{alias}.{m}().seed(0)\n"
                new_code += f"{alias}.seed(0)\n"
            else:
              new_code += f"{alias}.{m}.seed(0)\n"
      except (ModuleNotFoundError, AttributeError):
        pass
    else:
      new_code += line + "\n"

  # Remove incorrect seed setting codes
  lines = list(set(new_code.splitlines()))
  lines.sort()
  for line in lines:
   if "F.torch.seed" in line:
    lines.remove(line)
  return lines

tff1=0

def main():
  source_code = input("Enter the source code file name: ")
  with open(source_code, "r") as f:
    source_code = f.read()

  if check_for_random_numbers(source_code):
    new_code = initialize_seeds(source_code)
    for i in new_code:
     print(i)
  else:
    print("The source code does not contain random numbers.")

if __name__ == "__main__":
 main()

