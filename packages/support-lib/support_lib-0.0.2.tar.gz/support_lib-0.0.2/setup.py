import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name="support_lib",
	version="0.0.2",
	author="DarrenWhite",
	author_email="darren.white@ims-evolve.com",
	packages=["support_lib"],
	description="A sample test package",
	long_description=description,
	long_description_content_type="text/markdown",
	url="https://bitbucket.org/teamims/support-lib/src/main/",
	license='MIT',
	python_requires='>=3.10',
	install_requires=['jira==3.8.0',
                      'opsgenie-sdk==2.1.5',
                      'oracledb==1.3.2',
                      'mysql-connector==2.2.9']
)
