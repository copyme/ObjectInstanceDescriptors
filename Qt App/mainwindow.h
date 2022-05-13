#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>


// CGAL deps
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Point_set_3.h>
#include <CGAL/draw_point_set_3.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/point_generators_3.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <CGAL/Search_traits_3.h>
#include <CGAL/Qt/Basic_viewer_qt.h>
#include <QListWidget>
#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>
#include <CGAL/Polygon_mesh_processing/distance.h>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
// TYPES
    typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
    typedef K::FT FT;
    typedef K::Point_3 Point;
    typedef K::Plane_3 Plane;
    typedef K::Vector_3 Vector;
    typedef K::Segment_3 Segment;
    typedef K::Triangle_3 Triangle;
    typedef K::Iso_cuboid_3 Iso;
    typedef CGAL::Point_set_3<Point> Point_set;

    typedef CGAL::Surface_mesh<Point> Surface_mesh;
    typedef CGAL::Search_traits_3<K> TreeTraits;
    typedef CGAL::Orthogonal_k_neighbor_search<TreeTraits> Neighbor_search;
    typedef Neighbor_search::Tree Tree;
    typedef std::list<Point> SampledSet;


    FT compute_area(Surface_mesh& mesh);
    void sample_mesh(const Surface_mesh &input_mesh);
    void enlarge(Iso& bbox, const FT ratio);

public slots:
    void Select_classes();

public slots:
    void open_classes();
    void open_lidar();
    void cliquer(QListWidgetItem *item);
    void some_stat();
    void teste();

    void teste2();




private:
    Ui::MainWindow *ui;
    Point_set lidar_point_set;
    Point p;
    Point_set nearest_point_set;
    void kd_tree(Point_set &lidar_point_set);
    CGAL::Basic_viewer_qt * pointViewer;

    void add_point23DView(CGAL::Basic_viewer_qt * viewer, const Point & p, const CGAL::IO::Color & c);

    template<typename Iter>
    void show_PointSet(CGAL::Basic_viewer_qt * viewer, const Iter & begin, const Iter & end, const CGAL::IO::Color & c);

    QSlider *HzSlider;

    QLabel *HzSliderValue;

    Iso class_tmp_bbox;
    Tree tree_lidar;
    SampledSet class_sampled_points;

};
#endif // MAINWINDOW_H
