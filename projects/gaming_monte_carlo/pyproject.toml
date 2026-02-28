[project]
name = "gaming-monte-carlo"
version = "0.1.0"
description = "Monte Carlo simulation tools for Idleon mechanics."
readme = "README.md"
requires-python = ">=3.14.2"
dependencies = [
  "numpy>=2.0.0",
]

[project.scripts]
gaming-monte-carlo = "gaming_monte_carlo.main:main"

[tool.black]
line-length = 100
target-version = ["py314"]

[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["gaming_monte_carlo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"

# Autoflake is typically run via CLI, but these args are the ones we expect:
# autoflake --remove-all-unused-imports --remove-unused-variables --in-place -r src tests
