from setuptools import setup, Extension

setup(
    name='emotions_analysis_c',  # Nome do seu pacote
    version='1.0.0',            # Versão do seu pacote
    ext_modules=[
        Extension('emotions_analysis_c', ['emotions_analysis_c.c']),
    ],
)
