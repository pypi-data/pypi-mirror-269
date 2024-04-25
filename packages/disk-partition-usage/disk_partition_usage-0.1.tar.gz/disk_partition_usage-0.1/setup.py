from setuptools import setup, find_packages

setup(
    name='disk_partition_usage',
    version='0.1',
    packages=['disk_partition_usage'],
    entry_points={
        'console_scripts': [
            'get_disk_info=disk_partition_usage.disk_usage:get_disk_info_main',
        ],
    },
)
