from setuptools import setup, find_packages

setup(
    name='CoreStart',
    version='0.1.3',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    url='https://github.com/data-jeong/CoreStart',
    entry_points={
        'console_scripts': [
            'core_start=corestart.core_start:run',
        ],
    },
    install_requires=[
        # 여기에 필요한 의존성을 추가
    ],
    python_requires='>=3.6',
)

