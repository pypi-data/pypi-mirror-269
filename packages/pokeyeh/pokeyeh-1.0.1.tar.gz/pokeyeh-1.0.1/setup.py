from setuptools import setup, find_packages

setup(
       name="pokeyeh",
       version= "1.0.1",
       author="Pablo Lozher",
       author_email="lozadapablo85@gmail.com",
       description="Libreria para generar un pokemon aleatorio.",
       packages=["pokeyeh"],
       package_data={'pokeyeh' :["pokemon.csv"]},
       install_requires=[
             'pandas'
       ]
)