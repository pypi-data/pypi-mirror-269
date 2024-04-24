from setuptools import setup
import setuptools

setup(name='celldetective',
			version='1.0.2',
			description='description',
			long_description=open('README.rst').read(),
			long_description_content_type='text/markdown',
			url='http://github.com/remyeltorro/celldetective',
			author='Rémy Torro',
			author_email='remy.torro@inserm.fr',
			license='GPL-3.0',
			packages=setuptools.find_packages(),
			zip_safe=False,
			package_data={'celldetective': ['*','scripts/*','gui/*','models/*/*/*','models/*','models/*/*','icons/*','links/*','datasets/*', 'datasets/*/*']},
			entry_points = {
				'console_scripts': [
					'celldetective = celldetective.__main__:main']
		 }
			)

