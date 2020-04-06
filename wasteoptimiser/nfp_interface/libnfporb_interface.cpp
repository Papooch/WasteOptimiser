#include "libnfporb.hpp"

#include <vector>
#include <tuple>
#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace libnfporb;
using namespace std;

polygon_t convertToPolygon(vector<pair<double, double>> poly) {
	polygon_t rp;
	for (auto p : poly) {
		rp.outer().push_back(point_t(get<0>(p), get<1>(p)));
	}

	return rp;
}
vector<vector<pair<double, double>>> convertFromPolygon(vector<polygon_t::ring_type> polys) {
	vector<vector<pair<double, double>>> ret;
	for (auto poly : polys) {
		vector<pair<double, double>> rng;
		for (auto point : poly) {
			pair<double,double> tpl = make_pair((double) point.x_.val(), (double) point.y_.val() );
			rng.push_back(tpl);
		}
		ret.push_back(rng);
	}
	return ret;
}

vector<vector<pair<double, double>>> genNFP(vector<pair<double, double>> inA, vector<pair<double, double>> inB) {
	polygon_t pA = convertToPolygon(inA);
	polygon_t pB = convertToPolygon(inB);

	nfp_t nfp = generateNFP(pA, pB, false);
	
	return convertFromPolygon(nfp);
}

PYBIND11_MODULE(libnfporb_interface, m) {
	m.def("genNFP", &genNFP, R"pbdoc(computes tanh)pbdoc");
	m.attr("__version___") = "dev";
}