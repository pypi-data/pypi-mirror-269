python -m build
python -m twine upload --repository pypi dist/*
pip uninstall mimllearning -y
pip install mimllearning
