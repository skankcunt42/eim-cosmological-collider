from setuptools import setup, find_packages

setup(
    name="eim-cosmological-collider",
    version="0.1.0",
    description="Tri-Lobe EIM Simulation for W.43 Seam Audit",
    author="Thomas P. Connelly Jr. with Grok",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["networkx", "numpy", "matplotlib", "scipy"],
    python_requires=">=3.8",
)
