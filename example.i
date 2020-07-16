%module example
%{
#include "example.h"
%}

%include "std_vector.i"
%include "std_pair.i"
%include "std_map.i"
%include "std_string.i"
// Instantiate templates used by example
namespace std {
   %template(IntVector) vector<int>;
   %template(DoubleVector) vector<double>;
    %template(pairintint) pair<int,int>;
    %template(vectorpairintint) vector<pair<int,int>>;
    %template(vectorpairdoublevector) vector<pair<double,vector<int>>>;
    %template(mapstringint) map<string,int>;
    %template(vectorvector) vector<vector<int>>;
}

// Include the header file with above prototypes
%include "example.h"