#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QMessageBox>
#include <QFileDialog>
#include <iostream>
#include <QVBoxLayout>
#include <QPushButton>
#include <QDir>
#include <QStandardPaths>
#include <vector>
#include <CGAL/Point_set_3.h>
#include <CGAL/Point_set_3/IO.h>
#include <CGAL/IO/read_ply_points.h>
#include <CGAL/IO/write_ply_points.h>
#include <CGAL/bounding_box.h>
#include <QHBoxLayout>



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)

{

    srand(time(0));
    //QListWidgetItem *item = new QListWidgetItem;
    ui->setupUi(this);
    setWindowTitle(" My application ");
    pointViewer = new CGAL::Basic_viewer_qt(nullptr, "test",  true, true, true, false, true);
    ui->for3DViewer->addSubWindow(pointViewer);
    pointViewer->show();
    //ui->listWidget->setSelectionMode(QAbstractItemView::MultiSelection);  To select several files



}

MainWindow::~MainWindow()
{
    delete ui;
}


namespace PMP = CGAL::Polygon_mesh_processing;



void MainWindow::help_button()
{
    QStringList filelist = QFileDialog::getOpenFileNames(this,tr("Open file"),"C:\\Users\\taguilar\\Documents\\Project\\data","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");


    for(QList<QString>::const_iterator it=filelist.begin(); it!= filelist.end(); it++){

        new QListWidgetItem(*it, ui->listWidget);
        lidar_point_set.clear();
        if(!CGAL::IO::read_point_set(it->toStdString(), lidar_point_set))
        {
          throw std::runtime_error("Can't read input file " + it->toStdString());
        }
        show_PointSet(pointViewer, lidar_point_set.point_map().begin(), lidar_point_set.point_map().end(), CGAL::IO::Color(rand()%256, rand()%256, rand()%256));

    }

}
    //QMessageBox msgBox;
    //msgBox.setText(" Just a Test :) ");
    //msgBox.exec();



void MainWindow::open_classes()

{

    QString dirPath = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                    "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix",
                                                    QFileDialog::ShowDirsOnly
                                                    | QFileDialog::DontResolveSymlinks);
    //QStandardPaths::displayName(QStandardPaths::HomeLocation)

    if(dirPath.size() == 0)
        return;

    QDir dir(dirPath);
    foreach(QFileInfo var, dir.entryInfoList())
    {

        new QListWidgetItem(var.absoluteFilePath(), ui->listWidget);

    }
}

void MainWindow::open_lidar()
{
    QString file_name = QFileDialog::getOpenFileName(this,tr("Open file"),"C:\\Users\\taguilar\\Documents\\Project\\data","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");
    //QStandardPaths::displayName(QStandardPaths::HomeLocation)

    if(file_name==0){
        return;
    }
    lidar_point_set.clear();
    if(!CGAL::IO::read_point_set(file_name.toStdString(), lidar_point_set))
    {
      throw std::runtime_error("Can't read input file " + file_name.toStdString());
    }
    show_PointSet(pointViewer, lidar_point_set.point_map().begin(), lidar_point_set.point_map().end(), CGAL::IO::Color(100,100,100,70));

}


////////////////////////////// TEST ////////////////////////////////////
///////////////////////////////////////////////////////////////////////


void MainWindow::sample_mesh(const Surface_mesh & input_mesh)
{
    double density = ui -> SliderDensity -> value();
    class_sampled_points.clear();

    std::cout << "density: " << density << std::endl;
    // read input mesh

     // sample mesh uniformly
    std::list<Surface_mesh> components;
    std::cout << "sample... ";
    PMP::sample_triangle_mesh(input_mesh, std::back_inserter(class_sampled_points),
        PMP::parameters::number_of_points_per_area_unit(density));
    std::cout << "done (" << class_sampled_points.size() << " point samples)" << std::endl;

    // compute bounding box of samples
    std::cout << "compute bounding box... ";
    class_tmp_bbox = CGAL::bounding_box(class_sampled_points.begin(), class_sampled_points.end());
    std::cout << "done (" << class_tmp_bbox << ")" << std::endl;



}

void MainWindow::kd_tree(Point_set & lidar_point_set)
{
    // compute KD-tree
    std::cout << "compute kd-tre... ";
    tree_lidar.clear();
    tree_lidar.insert(lidar_point_set.point_map().begin(), lidar_point_set.point_map().end());
    std::cout << "done" << std::endl;
}

void MainWindow::some_stat()
{

    Point_set nearest_point_set;
    // compute distance statistics between mesh-samples and the cloud
    FT dmin = std::numeric_limits<double>::max();
    FT dmax = 0.0;
    std::vector<FT> distances; // store all distances
    std::list<Point>::iterator sit;
    std::cout << "compute statistics... ";
    for (sit = class_sampled_points.begin(); sit != class_sampled_points.end(); sit++)
    {
        // compute distance between current sample and nearest point from cloud
        Point& query = *sit;
        Neighbor_search search(tree_lidar, query, 1); // 1 = one nearest neighbor search
        Neighbor_search::iterator it = search.begin();

        // compute distance
        const FT d = std::sqrt(it->second);
        dmin = std::min(d, dmin);
        dmax = std::max(d, dmax);
        distances.push_back(d);

        Point nearest_point = it->first;
        // Create new point set with nearest points
        nearest_point_set.insert (nearest_point);
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

   CGAL::IO::Color random_color(rand()%256, rand()%256, rand()%256);
   show_PointSet(pointViewer, nearest_point_set.point_map().begin(), nearest_point_set.point_map().end(), random_color);
   pointViewer->show();

    CGAL::Basic_viewer_qt* tmpViewer = new CGAL::Basic_viewer_qt(nullptr, "nearest points",  true, true, true, false, true);
    ui->for3DViewer->addSubWindow(tmpViewer);
    CGAL::IO::Color tmp_color(0,255,0);
    show_PointSet(tmpViewer, nearest_point_set.point_map().begin(), nearest_point_set.point_map().end(), tmp_color);
    tmpViewer->show();
}

void MainWindow::cliquer(QListWidgetItem *item)
{
    if (lidar_point_set.empty())
    {
        QMessageBox msgBox;
        msgBox.setText("You need to load the LIDAR data first!");
        msgBox.exec();
        return;
    }

    if(item->isSelected())
    {

        //First Test
        //item->setText("Change name ");
        //item->setTextColor(Qt::red);

        //double density = 1e4;
        std::cout << "mesh filename: " << item << std::endl;
        Surface_mesh input_mesh;
        //std::string mesh_file_name(item->text());
        std::cout << "read mesh... ";
        if (!PMP::IO::read_polygon_mesh(item->text().toStdString(), input_mesh) ||
            is_empty(input_mesh) || !is_triangle_mesh(input_mesh))
        {
            QMessageBox msgBox;
            msgBox.setText("The element is not a mesh!");
            msgBox.exec();
            return;
        }
        std::cout << "done (" << input_mesh.number_of_faces() << " facets)" << std::endl;


        // sample mesh uniformly :
        sample_mesh(input_mesh);
        CGAL::Basic_viewer_qt* tmpViewer = new CGAL::Basic_viewer_qt(nullptr, "test",  true, true, true, false, true);
        ui->for3DViewer->addSubWindow(tmpViewer);
        CGAL::IO::Color tmp_color(0,0,255);
        show_PointSet(tmpViewer, class_sampled_points.cbegin(), class_sampled_points.cend(), tmp_color);
        tmpViewer->show();

        //compute Kd-Tree :
        kd_tree(lidar_point_set);

        //compute distance statistics between mesh-samples and the cloud
        some_stat();




        // Show presence mesh to for3DViewer :
      //  CGAL::IO::Color random_color(rand()%256, rand()%256, rand()%256);
        //pointViewer = new CGAL::Basic_viewer_qt(nullptr, "test",  true, true, true, false, true);
     //   show_PointSet(pointViewer, class_sampled_points.cbegin(), class_sampled_points.cend(), random_color);

        //ui->for3DViewer->addSubWindow(pointViewer);
        //pointViewer->show();




    }
}








///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
///
///
void MainWindow::add_point23DView(CGAL::Basic_viewer_qt * viewer, const Point &p, const CGAL::IO::Color & c)
{
    viewer->add_point(p, c);
}


template<typename Iter>
void MainWindow::show_PointSet(CGAL::Basic_viewer_qt * viewer, const Iter & begin, const Iter & end, const CGAL::IO::Color & c)
{
    for (Iter it = begin; it != end; it++)
    {
        add_point23DView(viewer, *it, c);
    }


    auto bbx = viewer->bounding_box();
    viewer->camera()->
        setSceneBoundingBox(CGAL::qglviewer::Vec(bbx.xmin(),
                                                 bbx.ymin(),
                                                 bbx.zmin()),
                            CGAL::qglviewer::Vec(bbx.xmax(),
                                                 bbx.ymax(),
                                                 bbx.zmax()));
    viewer->showEntireScene();
    viewer->redraw();
}
