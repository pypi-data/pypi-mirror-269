from setuptools import find_packages, setup

setup(
    name="pdf_tools_sdk",
    version="1.5.0-rc.3",
    packages=find_packages(),
    description="Python package for Pdftools SDK",
    package_data={
        "pdf_tools_sdk": [
            "lib/linux-x64/*.so",
            "lib/osx-arm64/*.dylib",
            "lib/osx-x64/*.dylib",
            "lib/win-x64/*.dll",
            "lib/win-x86/*.dll",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
