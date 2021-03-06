# -*- coding:utf-8 -*-

# from distutils.core import setup, Extension
#
# # define the extension module
# cos_module = Extension('cos_module', sources=['cos_module.c'])
#
# # run the setup
# setup(ext_modules=[cos_module])

# http://segmentfault.com/a/1190000000479951
# python setup.py build_ext --inplace running build_ext

# build_ext是用来构建扩展模块的
# --inplace将编译好的扩展模块输出到当前文件夹
# 文件cos_module.so包含编译的扩展，我们能将它加载到IPython解释器中：


# from distutils.core import setup, Extension
# from Cython.Distutils import build_ext
#
# setup(
#     cmdclass={'build_ext': build_ext},
#     ext_modules=[Extension("cy_rolling_dd_custom_mv", ["_cy_rolling_dd_custom_mv.pyx"])]
# )


from distutils.core import setup, Extension

import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("cy_rolling_dd_custom_mv",
                           sources=["cy_rolling_dd_custom_mv.pyx"],
                           # sources=["_cy_rolling_dd_custom_mv.pyx", "cy_rolling_dd_custom_mv.c"],
                           include_dirs=[numpy.get_include()])],
)

# python setup.py build_ext --inplace running build_ext

# http://segmentfault.com/a/1190000000479951
