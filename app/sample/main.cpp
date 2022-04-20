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

#include <CGAL/IO/write_xyz_points.h>
#include <CGAL/IO/write_ply_points.h>

// kernel
using Kernel = CGAL::Exact_predicates_inexact_constructions_kernel;
using FT = Kernel::FT;
using Point_3 = Kernel::Point_3;
using Plane_3 = Kernel::Plane_3;
using Vector_3 = Kernel::Vector_3;
using Segment_3 = Kernel::Segment_3;
using Triangle_3 = Kernel::Triangle_3;
using Iso_cuboid_3 = Kernel::Iso_cuboid_3;


// surface mesh
using Surface_mesh = CGAL::Surface_mesh<Point_3>;

// AABB tree
typedef std::list<Triangle_3>::iterator Iterator;
typedef CGAL::AABB_triangle_primitive<Kernel, Iterator> Primitive;
typedef CGAL::AABB_traits<Kernel, Primitive> AABB_triangle_traits;
typedef CGAL::AABB_tree<AABB_triangle_traits> Tree;

FT compute_area(Surface_mesh& mesh);

// usage
void usage()
{
    std::cout << "Sample mesh with points" << std::endl;
    std::cout << "Usage: sample -i input_mesh -d density -o out_file_name" << std::endl;
    std::cout << "Reads OFF/STL/OBJ/PLY/TS/VTP files only" << std::endl;
    std::cout << "density = number of sample points per area unit" << std::endl;
}

namespace PMP = CGAL::Polygon_mesh_processing;

int main(int argc, char** argv)
{
    const int argc_check = argc - 1;
    char* mesh_file_name_ptr = nullptr;
    const char* out_file_name = "out.ply";

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
            mesh_file_name_ptr = argv[++i];
        else if (!strcmp("-d", argv[i]) && i < argc_check)
            density = std::stod(argv[++i]);
        else if (!strcmp("-o", argv[i]) && i < argc_check)
            out_file_name = argv[++i];
    }

    std::cout << "density: " << density << std::endl;

    // read input mesh
    Surface_mesh input_mesh;
    std::string mesh_file_name(mesh_file_name_ptr);
    std::cout << "read mesh... ";
    if (!PMP::IO::read_polygon_mesh(mesh_file_name, input_mesh) ||
        is_empty(input_mesh) ||
        !is_triangle_mesh(input_mesh))
    {
        std::cerr << "Invalid mesh input" << std::endl;
        return EXIT_FAILURE;
    }
    std::cout << "done (" << input_mesh.number_of_faces() << " facets)" << std::endl;

    // compute total area
    const FT area = compute_area(input_mesh);
    std::cout << "total area: " << area << std::endl;

    // sample mesh uniformly
    std::list<Surface_mesh> components;
    std::cout << "sample... ";
    std::list<Point_3> samples;
    PMP::sample_triangle_mesh(input_mesh, std::back_inserter(samples),
        PMP::parameters::number_of_points_per_area_unit(density));
    std::cout << "done (" << samples.size() << " point samples)" << std::endl;

    // save samples to file
    std::cout << "save samples to file " << out_file_name << "... ";
    CGAL::IO::write_PLY(out_file_name, samples);
    std::cout << "done" << std::endl;

    return EXIT_SUCCESS;
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
        Point_3& p0 = get(vpm, source(he, mesh));
        Point_3& p1 = get(vpm, target(he, mesh));
        Point_3& p2 = get(vpm, target(next(he, mesh), mesh));
        Triangle_3 triangle(p0, p1, p2);
        sum_areas += std::sqrt(triangle.squared_area());
    }
    return sum_areas;
}