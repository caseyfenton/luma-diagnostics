from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

test_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pillow>=8.3.1",  # For image validation
]

setup(
    name="luma-diagnostics",
    version="0.1.0",
    author="LUMA Labs",
    author_email="support@lumalabs.ai",
    description="A diagnostic tool for troubleshooting LUMA Dream Machine API issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lumalabs/api-diagnostics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "test": test_requirements,
    },
    entry_points={
        "console_scripts": [
            "luma-diagnostics=luma_diagnostics.cli:main",
        ],
    },
    package_data={
        "luma_diagnostics": [
            "templates/*",
            "cases/templates/*"
        ],
    },
)
