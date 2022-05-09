#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>


// CGAL deps
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Point_set_3.h>
#include <CGAL/draw_point_set_3.h>

#include <CGAL/point_generators_3.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <CGAL/Search_traits_3.h>

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
    typedef K::Vector_3 Vector;
    typedef CGAL::Point_set_3<Point> Point_set;

    typedef CGAL::Search_traits_3<K> TreeTraits;
    typedef CGAL::Orthogonal_k_neighbor_search<TreeTraits> Neighbor_search;
    typedef Neighbor_search::Tree Tree;


public slots:
    void help_button();

public slots:
    void open_classes();
    void get_name();
    void open_lidar();

private:
    Ui::MainWindow *ui;
    Point_set source_point_set;
};
#endif // MAINWINDOW_H
