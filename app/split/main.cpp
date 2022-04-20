#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Surface_mesh.h>
#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>

#include <CGAL/Timer.h>
#include <CGAL/bounding_box.h>

#include <CGAL/AABB_tree.h>
#include <CGAL/AABB_traits.h>
#include <CGAL/AABB_triangle_primitive.h>


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



// usage
void usage()
{
    std::cout << "Split mesh into components\n"
        "Usage: split -i input_mesh\n" <<
        "Reads OFF/STL/OBJ/PLY/TS/VTP files only. \n";
}


int main(int argc, char** argv)
{
    const int argc_check = argc - 1;
    char* mesh_file_name_ptr = nullptr;

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
    }


    // read input mesh
    Surface_mesh input_mesh;
    std::string mesh_file_name(mesh_file_name_ptr);
    std::cout << "read mesh...";
    if (!CGAL::Polygon_mesh_processing::IO::read_polygon_mesh(mesh_file_name, input_mesh) ||
        is_empty(input_mesh) ||
        !is_triangle_mesh(input_mesh))
    {
        std::cerr << "Invalid mesh input" << std::endl;
        return EXIT_FAILURE;
    }
    std::cout << "done (" << input_mesh.number_of_faces() << " facets)" << std::endl;

    // split connected components
    std::list<Surface_mesh> components;
    std::cout << "split into components...";
    CGAL::Polygon_mesh_processing::split_connected_components(input_mesh, components);
    std::cout << "done (" << components.size() << " components)" << std::endl;

    // save components
    int index = 0;
    std::list<Surface_mesh>::iterator it;
    for (it = components.begin(); it != components.end(); it++, index++)
    {
        Surface_mesh& mesh = *it;

        // generate file name
        std::string name("component-");
        name.append(std::to_string(index)).append(".ply");

        // save component to file
        std::cout << "save to file " << name << "...";
        if (!CGAL::IO::write_polygon_mesh(name, mesh, CGAL::parameters::stream_precision(17)))
        {
            std::cout << "unable to write output mesh" << std::endl;
            return EXIT_FAILURE;
        }
        std::cout << "done" << std::endl;
    }

    return EXIT_SUCCESS;
}



/*
// fill triangles with triangle facets from input mesh
// and points with its vertices
std::list<Point_3> points;
std::list<Triangle_3> triangles;

auto vpm = get(CGAL::vertex_point, input_mesh);
typedef boost::graph_traits<Surface_mesh>::face_descriptor face_descriptor;
typedef boost::graph_traits<Surface_mesh>::halfedge_descriptor halfedge_descriptor;

for(face_descriptor f : faces(input_mesh))
{
  halfedge_descriptor he = halfedge(f, input_mesh);
  Point_3& p0 = get(vpm, source(he, input_mesh));
  Point_3& p1 = get(vpm, target(he, input_mesh));
  Point_3& p2 = get(vpm, target(next(he, input_mesh), input_mesh));
  triangles.push_back(Triangle_3(p0, p1, p2));
  points.push_back(p0);
  points.push_back(p1);
  points.push_back(p2);
}

// build AABB tree
Tree tree(triangles.begin(), triangles.end());

// compute bounding box
std::list<Point_3> queries;
Iso_cuboid_3 c3 = CGAL::bounding_box(points.begin(), points.end());
*/