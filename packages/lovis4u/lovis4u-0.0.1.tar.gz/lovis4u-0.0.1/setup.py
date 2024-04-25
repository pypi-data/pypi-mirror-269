import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files("lovis4u/lovis4u_data")
extra_files.append("docs/pypi.md")

setuptools.setup(name="lovis4u",
                 version="0.0.1",
                 description="A tool for short uORF annotation.",
                 url="https://art-egorov.github.io/lovis4u/",
                 author="Artyom Egorov",
                 author_email="artem.egorov@med.lu.se",
                 license="WTFPL",
                 packages=["lovis4u"],
                 package_data={"lovis4u": extra_files},
                 install_requires=["biopython", "configs", "argparse", "distinctipy", "pandas", "reportlab",
                                   "bcbio-gff", "matplotlib", "seaborn", "scipy"],
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 scripts=["bin/lovis4u"],
                 zip_safe=False)
