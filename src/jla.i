// Author: Surhud More
// Email: surhudkicp@gmail.com
%module jla
%include "ini.i"
%feature("autodoc", 1);
%include "carrays.i"

%array_class(double, doubleArray);

%{
    #define SWIG_FILE_WITH_INIT
    #include "jla.h"
%}

%include "jla.h"
