# pylint: disable= missing-module-docstring
from setuptools import find_packages, setup

__version__ = "0.49.0"

# Default to PyQt6 if no other Qt binding is installed
QT_DEPENDENCY = "PyQt6>=6.0"
QSCINTILLA_DEPENDENCY = "PyQt6-QScintilla"

# pylint: disable=unused-import
try:
    import PyQt5
except ImportError:
    pass
else:
    QT_DEPENDENCY = "PyQt5>=5.9"
    QSCINTILLA_DEPENDENCY = "QScintilla"

if __name__ == "__main__":
    setup(
        install_requires=[
            "pydantic",
            "qtconsole",
            QT_DEPENDENCY,
            QSCINTILLA_DEPENDENCY,
            "jedi",
            "qtpy",
            "pyqtgraph",
            "bec_lib",
            "zmq",
            "h5py",
            "pyqtdarktheme",
            "black",
        ],
        extras_require={
            "dev": [
                "pytest",
                "pytest-random-order",
                "pytest-timeout",
                "coverage",
                "pytest-qt",
                "black",
                "isort",
            ],
            "pyqt5": ["PyQt5>=5.9"],
            "pyqt6": ["PyQt6>=6.0"],
        },
        version=__version__,
        packages=find_packages(),
        include_package_data=True,
        package_data={
            "": [
                "*.ui",
                "*.yaml",
                "*.png",
            ]
        },
    )
