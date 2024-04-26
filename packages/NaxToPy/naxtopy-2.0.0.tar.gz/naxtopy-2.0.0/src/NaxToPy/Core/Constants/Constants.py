"""Constants of the NaxToPy package"""

# NaxToPy Version
VERSION = "2.0.0"

# Supported for Naxto:
NAXTO_VERSION = '2024R1'
NAXTO_STEP = "0"

# Assembly version of NaxToModel.dll
VIZZER_COMPATIBILITY = ("4.1.0.0", "4.1.0.1")
"""Tuple with the compatible versions of NaxToModel.dll"""

# PYTHON EXTERNO ----------------------------------------------------------------------------------
# Versiones de Python soportadas:
SUP_PY_VER = (9, 10, 11, 12)

# Librerias Externas de Python
EXTERNAL_LIBS_PYTHON = ['cffi',
                        'clr_loader',
                        'pycparser',
                        'pythonnet',
                        'numpy',
                        'setuptools']
# -------------------------------------------------------------------------------------------------

# Binary extensions supported by NaxToPy ----------------------------------------------------------
BINARY_EXTENSIONS = ["op2", "xdb", "h5", "h3d", "odb", "rst"]

# NAXTO -------------------------------------------------------------------------------------------
# Ruta a las librerias de NaxTo
DEVELOPER_VIZZER = r'C:\GIT_REPOSITORIES\NAXTO\NAXTOVIEW\v.4.0\NaxToView\NaxToModel\bin\x64\Debug'

# DLLs de NaxTo
VIZZER_CLASSES_DLL = 'NaxToModel.dll'
# -------------------------------------------------------------------------------------------------

PEDIGREE_FACTOR = 1000  # Para pasar de id pedigree a id solver: id_solver = id_pedigree // _PEDIGREE_FACTOR_
                        # Para obtener el id part: id_pedigree % _PEDIGREE_FACTOR_


