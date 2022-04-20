#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Point_set_3.h>
#include <CGAL/draw_point_set_3.h>

#include <CGAL/point_generators_3.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <CGAL/Search_traits_3.h>
#include <list>
#include <cmath>

#include <iostream>
#include <fstream>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef K::FT FT;
typedef K::Point_3 Point;
typedef K::Vector_3 Vector;
typedef CGAL::Point_set_3<Point> Point_set;

typedef CGAL::Search_traits_3<K> TreeTraits;
typedef CGAL::Orthogonal_k_neighbor_search<TreeTraits> Neighbor_search;
typedef Neighbor_search::Tree Tree;


void point_set_to_list (const Point_set& point_set, std::list<Point>& points)
{
  std::cout << "Convert point set to list" << std::endl;
  for (Point_set::const_iterator it = point_set.begin();
       it != point_set.end(); ++ it)
    points.push_back(point_set.point(*it)); // can use point_set[it] instead of point_set.point(*it)
}

void print_list_to_csv(std::list<float> dist_list, const char* out_filename) {
  std::ofstream myfile;
  std::list<float>::iterator it;
  myfile.open (out_filename);

  for (it = dist_list.begin();
       it != dist_list.end(); it++)
  {
    myfile << *it << "\n";
  }
  myfile.close();
}

int main (int argc, char** argv)
{
  const int argc_check = argc - 1;
  const char* filename_1 = argc > 1 ? argv[1] : "sampled_element.ply";
  const char* filename_2 = argc > 2 ? argv[2] : "H0022-cloud-subsample-1cm.ply";
  const char* out_filename = "dist.csv";
  Point_set source_point_set;
  Point_set target_point_set;
  Point_set nearest_point_set;
  Point nearest_point;
  float nearest_dist;
  std::list<Point> target_point_list;
  std::list<float> dist_list;

  // Number of nearest neighbours
  const unsigned int N = 1;
  Point query;

  for (int i = 1; i < argc; ++i)
  {
    if (!strcmp("-o", argv[i]) && i < argc_check)
      out_filename = argv[++i];
  }

  std::cout << "Output file " << out_filename << std::endl;

  // Read input files and convert to point sets
  if(!CGAL::IO::read_point_set(filename_1, source_point_set))
  {
    std::cerr << "Can't read input file " << filename_1 << std::endl;
    return EXIT_FAILURE;
  }

  if(!CGAL::IO::read_point_set(filename_2, target_point_set))
  {
    std::cerr << "Can't read input file " << filename_2 << std::endl;
    return EXIT_FAILURE;
  }

  // Plot the first point set, which represents the sampled element 
  // that we want to detect in the point cloud (laser data)
  CGAL::draw(source_point_set);

  // We need first to create a list of points from point set to create a tree 
  point_set_to_list (target_point_set, target_point_list);

  // Create a tree (containing the target points) to speed the search
  Tree tree(target_point_list.begin(), target_point_list.end());
 
  std::cout << "Search for " << N << " nearest points" << std::endl;
 
  for (Point_set::const_iterator it = source_point_set.begin();
       it != source_point_set.end(); ++ it)
  {
    // Define new query origin from source point set
    query = source_point_set.point(*it);

    // Initialize the search structure, and search all N points
    Neighbor_search search(tree, query, N);

    // Report the first nearest neighbor and its distance
    Neighbor_search::iterator it_nbs = search.begin();
    nearest_point = it_nbs->first;
    nearest_dist = std::sqrt(it_nbs->second);

    // Create new point set with nearest points
    nearest_point_set.insert (nearest_point);

    // Create list with all distances
    dist_list.push_back(nearest_dist);
  }
  
  // Plot the new point set containing the nearest points in the target set, 
  // to check visually if it looks like the source point set
  CGAL::draw(nearest_point_set);

  // Save distances to file for statistics computation (later)
  std::cout << "Print distance values to file: " << out_filename << std::endl;
  print_list_to_csv(dist_list, out_filename);

  std::cout << "Done" << std::endl;
  
  return EXIT_SUCCESS;
}
