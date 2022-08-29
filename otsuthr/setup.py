from setuptools import Extension, setup
from Cython.Build import cythonize

sourcefiles = ['tgon.pyx']

extensions = [Extension("tgon", sourcefiles, 
        extra_compile_args=['-D_GLIBCXX_USE_CXX11_ABI=0'],
        include_dirs=['/usr/local/include/leptonica','/usr/local/include/tesseract','/home/rmast/tesseract/src/ccstruct','/home/rmast/tesseract/src/ccutil'],
        libraries=['tesseract','leptonica']
    )]

setup(
    ext_modules=cythonize(extensions,
        compiler_directives={'language_level' : "3"}
        )
)
