#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QMessageBox>
#include <QFileDialog>
#include <iostream>
#include <QVBoxLayout>
#include <QPushButton>
#include <QDir>
#include <QStandardPaths>

#include <CGAL/draw_point_set_3.h>



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)

{

    ui->setupUi(this);
    setWindowTitle(" My application ");

    //std::cout << file_name.toStdString() << std::endl;
    //QString file_name = QFileDialog::getOpenFileName(this,tr("Open file"),"C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");
    //ui->comboBox->addItem(file_name.toStdString());
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::help_button()
{
    QMessageBox msgBox;
    msgBox.setText(" Just a Test :) ");
    msgBox.exec();
}


void MainWindow::open_classes()

{

    QString dirPath = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                    QStandardPaths::displayName(QStandardPaths::HomeLocation),
                                                    QFileDialog::ShowDirsOnly
                                                    | QFileDialog::DontResolveSymlinks);
    QDir dir(dirPath);
    foreach(QFileInfo var, dir.entryInfoList())
    {
        //ui->comboBox->addItem(var.absoluteFilePath());
        new QListWidgetItem(var.absoluteFilePath(), ui->listWidget);

    }
    //QString file_name = QFileDialog::getOpenFileName(this,tr("Open file"),"C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");
    //QMessageBox::information(this,'..',file_name);
    //new QListWidgetItem(file_name, ui->listWidget);


}

void MainWindow::open_lidar()
{
    QString file_name = QFileDialog::getOpenFileName(this,tr("Open file"),"C:\\Users\\taguilar\\Documents\\Project\\data\\","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");
    new QListWidgetItem(file_name, ui->listWidget);

    if(!CGAL::IO::read_point_set(file_name.toStdString(), source_point_set))
    {
      throw std::runtime_error("Can't read input file " + file_name.toStdString());
    }

    CGAL::SimplePointSetViewerQt<Point_set > mainwindow(ui->openGLWidget, source_point_set, "source set");

}



void MainWindow::get_name()
{
    std::string file_name="C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all\\0762_x_2032mm_0762_x_2032mm_[147585].ply";
    std::cout<< file_name<<std::endl;
}




//void MainWindow::getsavefilename()
//{
//    QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"),
//                               "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\","All Files (*.*);;Ply files (*.ply);;Off files (*.off)");
//}


//QDir::homePath()
//"C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all\\");
//,"All Files (*.*);;Ply files (.ply);;Off files (.off)"
//QDir dir("C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\");
//foreach(QFileInfo var, dir.entryInfoList())
//{
//    ui->comboBox->addItem(var.absoluteFilePath());

//}

//ui->comboBox->addItem(file_name.toStdString());
//std::cout << file_name.toStdString() << std::endl;
