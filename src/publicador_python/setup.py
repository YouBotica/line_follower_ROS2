from setuptools import setup

package_name = 'publicador_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='legacy',
    maintainer_email='email@email.com',
    description='Publicador de cmd en python',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publicador_cmd = publicador_python.publicador_cmd:main',
            'subscriber_odom = publicador_python.subscriber_odom:main',
        ],
    },
)
