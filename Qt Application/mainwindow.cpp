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
    show_PointSet(pointViewer, lidar_point_set.point_map().begin(), lidar_point_set.point_map().end(), CGAL::IO::Color(rand()%256, rand()%256, rand()%256));
}


////////////////////////////// TEST ////////////////////////////////////
///////////////////////////////////////////////////////////////////////
void MainWindow::presence_code()
{
    //QListWidgetItem *item = ui->listWidget->currentItem();
    //item->setText("PETIT TEST");

    for(int i=0;i<10;i++){
        ui->listWidget->addItem(QString::number(i)+"item");
    }
    //QListWidgetItem *item;

}






//
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


        // sample mesh uniformly
        sample_mesh(input_mesh);
        CGAL::Basic_viewer_qt* tmpViewer = new CGAL::Basic_viewer_qt(nullptr, "test",  true, true, true, false, true);
        ui->for3DViewer->addSubWindow(tmpViewer);
        CGAL::IO::Color tmp_color(0,0,255);
        show_PointSet(tmpViewer, class_sampled_points.cbegin(), class_sampled_points.cend(), tmp_color);
        tmpViewer->show();




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
