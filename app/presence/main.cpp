#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Surface_mesh.h>
#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>
#include <CGAL/Polygon_mesh_processing/distance.h>

#include <CGAL/Timer.h>
#include <CGAL/bounding_box.h>

#include <CGAL/AABB_tree.h>
#include <CGAL/AABB_traits.h>
#include <CGAL/AABB_triangle_primitive.h>

#include <CGAL/bounding_box.h>

#include <CGAL/boost/graph/IO/OFF.h>

#include <string>
#include <algorithm>

#include <CGAL/Point_set_3.h>
#include <CGAL/Point_set_3/IO.h>
#include <CGAL/IO/read_ply_points.h>
#include <CGAL/IO/write_ply_points.h>

#include "console_color.h"


#define _SILENCE_EXPERIMENTAL_FILESYSTEM_DEPRECATION_WARNING
#include <experimental/filesystem>

// kernel
using Kernel = CGAL::Exact_predicates_inexact_constructions_kernel;
using FT = Kernel::FT;
using Point = Kernel::Point_3;
using Plane = Kernel::Plane_3;
using Vector = Kernel::Vector_3;
using Segment = Kernel::Segment_3;
using Triangle = Kernel::Triangle_3;
using Iso_cuboid = Kernel::Iso_cuboid_3;


// surface mesh
using Surface_mesh = CGAL::Surface_mesh<Point>;

// KD tree for K nearest neighbor search
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <CGAL/Search_traits_3.h>
typedef CGAL::Search_traits_3<Kernel> TreeTraits;
typedef CGAL::Orthogonal_k_neighbor_search<TreeTraits> Neighbor_search;
typedef Neighbor_search::Tree Tree;


FT compute_area(Surface_mesh& mesh);

// usage
void usage()
{
	std::cout << "Detect presence of meshed-element in point cloud" << std::endl;
	std::cout << "Parse all ply mesh files in current folder" << std::endl;
	std::cout << "The input meshed elements are sampled with user-specified density (number of samples per area unit)" << std::endl;
	std::cout << "Usage: sample -i point-set.ply -d density" << std::endl;
	std::cout << "Reads PLY files only" << std::endl;
	std::cout << "density = number of sample points per area unit" << std::endl;
}

namespace PMP = CGAL::Polygon_mesh_processing;

void enlarge(Iso_cuboid& bbox, const FT ratio);
bool analyze_mesh(std::string& mesh_file_name, Tree& tree, const double density);


int main(int argc, char** argv)
{
	const int argc_check = argc - 1;
	char* point_cloud_file_name = nullptr;

	double density = 1e4;

	// parse parameters
	if (argc < 2)
	{
		usage();
		return EXIT_FAILURE;
	}
	for (int i = 1; i < argc; ++i)
	{
		if (!strcmp("-h", argv[i]))
		{
			usage();
			return EXIT_FAILURE;
		}
		else if (!strcmp("-i", argv[i]) && i < argc_check)
			point_cloud_file_name = argv[++i];
		else if (!strcmp("-d", argv[i]) && i < argc_check)
			density = std::stod(argv[++i]);
	}

	std::cout << "point cloud filename: " << point_cloud_file_name << std::endl;
	std::cout << "density: " << density << std::endl;


	// read point-cloud file
	std::list<Point> cloud;
	std::cout << "read point cloud... ";
	std::ifstream input(point_cloud_file_name, std::ios::binary);
	CGAL::IO::read_PLY(input, std::back_inserter(cloud));
	std::cout << "done (" << cloud.size() << " points)" << std::endl;



	// compute KD-tree
	std::cout << "compute kd-tre... ";
	Tree tree(cloud.begin(), cloud.end());
	std::cout << "done" << std::endl;

	// parse all ply files in folder
	std::experimental::filesystem::path cpath = std::experimental::filesystem::current_path();
	std::string path = cpath.string();
	// std::cout << "path: " << path << std::endl;
	for (auto& entry : std::experimental::filesystem::directory_iterator(path))
	{
		std::string filename = entry.path().string();

		// skip point cloud
		if (filename.find("cloud") != std::string::npos)
			continue;

		if (filename.find(".ply") != std::string::npos)
			analyze_mesh(filename, tree, density);
	}

	return EXIT_SUCCESS;
}


bool analyze_mesh(std::string& mesh_file_name,
	Tree& tree,
	const double density)
{
	// read input mesh
	Surface_mesh input_mesh;

	std::cout << std::endl;
	std::cout << "read mesh " << mesh_file_name << "...";
	if (!PMP::IO::read_polygon_mesh(mesh_file_name, input_mesh) ||
		is_empty(input_mesh) ||
		!is_triangle_mesh(input_mesh))
	{
		std::cerr << "Invalid mesh input" << std::endl;
		return false;
	}
	std::cout << "done (" << input_mesh.number_of_faces() << " facets)" << std::endl;

	// compute total area
	const FT area = compute_area(input_mesh);
	std::cout << "total area: " << area << std::endl;

	// sample mesh uniformly
	std::list<Surface_mesh> components;
	std::cout << "sample... ";
	std::list<Point> samples;
	PMP::sample_triangle_mesh(input_mesh, std::back_inserter(samples),
		PMP::parameters::number_of_points_per_area_unit(density));
	std::cout << "done (" << samples.size() << " point samples)" << std::endl;

	// compute bounding box of samples
	// std::cout << "compute bounding box... ";
	// Iso_cuboid bbox = CGAL::bounding_box(samples.begin(), samples.end());
	// std::cout << "done (" << bbox << ")" << std::endl;

	// enlarge bounding box
	// std::cout << "enlarge bounding box... ";
	// enlarge(bbox, 1.2);
	// std::cout << "done (" << bbox << ")" << std::endl;

	// compute distance statistics between mesh-samples and the cloud
	FT dmin = std::numeric_limits<double>::max();
	FT dmax = 0.0;
	std::vector<FT> distances; // store all distances
	std::list<Point>::iterator sit;
	std::cout << "compute statistics... ";
	for (sit = samples.begin(); sit != samples.end(); sit++)
	{
		// compute distance between current sample and nearest point from cloud
		Point& query = *sit;
		Neighbor_search search(tree, query, 1); // 1 = one nearest neighbor search
		Neighbor_search::iterator it = search.begin();

		// compute distance 
		const FT d = std::sqrt(it->second);
		dmin = std::min(d, dmin);
		dmax = std::max(d, dmax);
		distances.push_back(d);
	}
	std::cout << "done" << std::endl;

	// sort distances
	std::cout << "sort distances... ";
	std::sort(distances.begin(), distances.end());
	std::cout << "done" << std::endl;

	const FT median = distances[(size_t)(0.5 * distances.size())];
	const FT p80 = distances[(size_t)(0.8 * distances.size())];
	std::cout << "min distance: " << dmin << std::endl;
	std::cout << "max distance: " << dmax << std::endl;
	std::cout << "median distance: " << median << std::endl;
	std::cout << "percentile 80 distance: " << p80 << std::endl;

	// save statistics to file only for present elements

	if (median > 0.3) // 30cm
		return false;


	std::string out_file_name = mesh_file_name.substr(0, mesh_file_name.find_last_of('.')) + ".txt";
	std::cout << green;
	std::cout << "save stats to file " << out_file_name << "... ";
	std::ofstream fout(out_file_name);
	fout << "min distance: " << dmin << std::endl;
	fout << "max distance: " << dmax << std::endl;
	fout << "median distance: " << median << std::endl;
	fout << "percentile 80 distance: " << p80 << std::endl;
	std::cout << "done" << std::endl;
	std::cout << white;

	// save mesh to filename-present.off
	std::string present_file_name = mesh_file_name.substr(0, mesh_file_name.find_last_of('.')) + "-present.off";
	std::ofstream mesh_out(present_file_name);
	CGAL::IO::write_OFF(mesh_out, input_mesh);

	return true;
}

// enlarge bounding box by a factor - keep it centered
void enlarge(Iso_cuboid& bbox, const FT ratio)
{
	Point c1 = bbox.min();
	Point c2 = bbox.max();
	Point mm = CGAL::midpoint(c1, c2);
	Vector vec = 0.5 * (c2 - c1);
	bbox = Iso_cuboid(mm - ratio * vec, mm + ratio * vec);
}


// compute total area of mesh
FT compute_area(Surface_mesh& mesh)
{
	auto vpm = get(CGAL::vertex_point, mesh);
	typedef boost::graph_traits<Surface_mesh>::face_descriptor face_descriptor;
	typedef boost::graph_traits<Surface_mesh>::halfedge_descriptor halfedge_descriptor;

	FT sum_areas = 0.0;
	for (face_descriptor f : faces(mesh))
	{
		halfedge_descriptor he = halfedge(f, mesh);
		Point& p0 = get(vpm, source(he, mesh));
		Point& p1 = get(vpm, target(he, mesh));
		Point& p2 = get(vpm, target(next(he, mesh), mesh));
		Triangle triangle(p0, p1, p2);
		sum_areas += std::sqrt(triangle.squared_area());
	}
	return sum_areas;
}