import setuptools

setuptools.setup(
    name="tgate",
    version="v0.1.2",
    author="Wentian Zhang",
    author_email="zhangwentianml@gmail.com",
    description="T-GATE: Cross-Attention Makes Inference Cumbersome in Text-to-Image Diffusion Models.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HaozheLiu-ST/T-GATE/tree/releases/",
    package_dir={"": "src"},
    packages=setuptools.find_packages('src'),
    include_package_data=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "diffusers",
        "transformers",
        "DeepCache==0.1.1",
        "torch",
        "accelerate",
    ],
    python_requires='>=3.8.0',
)

