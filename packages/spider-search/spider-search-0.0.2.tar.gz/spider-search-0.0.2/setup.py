import setuptools

if __name__ == '__main__':
    install_requires = [
        'requests~=2.27.1',
        'selenium~=3.141.0'
    ]
    setuptools.setup(
        name='spider-search',
        version='0.0.2',
        description='Search resource from web page',
        url='https://gitee.com/dengshaolin/spider-search',
        python_requires='>=3.6',
        packages=setuptools.find_packages(exclude=['demo']),
        include_package_data=True,
        install_requires=install_requires
    )
