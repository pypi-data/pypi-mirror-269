from setuptools import setup

def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        text = f.read()
    return text

setup(
    name = 'CTkListbox',
    version = '1.4',
    description = "Customtkinter Listbox widget",
    license = "MIT",
    readme = "README.md",
    long_description = get_long_description('README.md'),
    long_description_content_type = "text/markdown",
    author = 'Akash Bora',
    url = "https://github.com/Akascape/CTkListbox",
    classifiers = [
        "License :: OSI Approved :: MIT License ",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords = ['customtkinter', 'tkinter', 'listbox-widget', 'listbox',
                'modern-listbox', 'option menu', 'list-box', 'ctklistbox'],
    packages = ["CTkListbox"],
    install_requires = ['customtkinter'],
    dependency_links = ['https://pypi.org/project/customtkinter/'],
    python_requires = '>=3.6',
)
