/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionFiles2;
    QAction *actionCaseStudy3;
    QAction *actionCaseStudy4;
    QAction *actionCaseStudy5;
    QAction *actionCaseStudy6;
    QAction *actionFile1;
    QAction *actionShow_Sampled_Points;
    QAction *actionShow_Bounding_Box;
    QAction *actionShow_Mesh;
    QAction *actionL2_Distance;
    QAction *actionCaseStudy2;
    QAction *actionCaseStudy3_2;
    QAction *actionCaseStudy4_2;
    QAction *actionCaseStudy5_2;
    QAction *actionCaseStudy6_2;
    QAction *actionAll_Classes;
    QAction *actionLIDAR_DATA;
    QWidget *centralwidget;
    QToolButton *toolButton;
    QWidget *widget;
    QSlider *horizontalSlider;
    QTextBrowser *textBrowser;
    QProgressBar *progressBar_1;
    QTextBrowser *textBrowser_2;
    QProgressBar *progressBar_2;
    QSlider *horizontalSlider_2;
    QPushButton *pushButton;
    QWidget *widget_2;
    QWidget *widget_3;
    QTextEdit *textEdit;
    QTextEdit *textEdit_2;
    QTextEdit *textEdit_3;
    QCheckBox *checkBox;
    QCheckBox *checkBox_2;
    QCheckBox *checkBox_3;
    QOpenGLWidget *openGLWidget;
    QListWidget *listWidget;
    QMenuBar *menuBar;
    QMenu *menuFiles;
    QMenu *menuOpen;
    QMenu *menuFolder;
    QMenu *menuMethods;
    QMenu *menuView_Classes;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1375, 920);
        actionFiles2 = new QAction(MainWindow);
        actionFiles2->setObjectName(QString::fromUtf8("actionFiles2"));
        actionCaseStudy3 = new QAction(MainWindow);
        actionCaseStudy3->setObjectName(QString::fromUtf8("actionCaseStudy3"));
        actionCaseStudy4 = new QAction(MainWindow);
        actionCaseStudy4->setObjectName(QString::fromUtf8("actionCaseStudy4"));
        actionCaseStudy5 = new QAction(MainWindow);
        actionCaseStudy5->setObjectName(QString::fromUtf8("actionCaseStudy5"));
        actionCaseStudy6 = new QAction(MainWindow);
        actionCaseStudy6->setObjectName(QString::fromUtf8("actionCaseStudy6"));
        actionFile1 = new QAction(MainWindow);
        actionFile1->setObjectName(QString::fromUtf8("actionFile1"));
        actionShow_Sampled_Points = new QAction(MainWindow);
        actionShow_Sampled_Points->setObjectName(QString::fromUtf8("actionShow_Sampled_Points"));
        actionShow_Bounding_Box = new QAction(MainWindow);
        actionShow_Bounding_Box->setObjectName(QString::fromUtf8("actionShow_Bounding_Box"));
        actionShow_Mesh = new QAction(MainWindow);
        actionShow_Mesh->setObjectName(QString::fromUtf8("actionShow_Mesh"));
        actionL2_Distance = new QAction(MainWindow);
        actionL2_Distance->setObjectName(QString::fromUtf8("actionL2_Distance"));
        actionCaseStudy2 = new QAction(MainWindow);
        actionCaseStudy2->setObjectName(QString::fromUtf8("actionCaseStudy2"));
        actionCaseStudy3_2 = new QAction(MainWindow);
        actionCaseStudy3_2->setObjectName(QString::fromUtf8("actionCaseStudy3_2"));
        actionCaseStudy4_2 = new QAction(MainWindow);
        actionCaseStudy4_2->setObjectName(QString::fromUtf8("actionCaseStudy4_2"));
        actionCaseStudy5_2 = new QAction(MainWindow);
        actionCaseStudy5_2->setObjectName(QString::fromUtf8("actionCaseStudy5_2"));
        actionCaseStudy6_2 = new QAction(MainWindow);
        actionCaseStudy6_2->setObjectName(QString::fromUtf8("actionCaseStudy6_2"));
        actionAll_Classes = new QAction(MainWindow);
        actionAll_Classes->setObjectName(QString::fromUtf8("actionAll_Classes"));
        actionLIDAR_DATA = new QAction(MainWindow);
        actionLIDAR_DATA->setObjectName(QString::fromUtf8("actionLIDAR_DATA"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        toolButton = new QToolButton(centralwidget);
        toolButton->setObjectName(QString::fromUtf8("toolButton"));
        toolButton->setGeometry(QRect(1220, 790, 151, 101));
        QFont font;
        font.setPointSize(20);
        font.setBold(true);
        font.setItalic(true);
        toolButton->setFont(font);
        widget = new QWidget(centralwidget);
        widget->setObjectName(QString::fromUtf8("widget"));
        widget->setGeometry(QRect(0, 790, 1201, 101));
        QPalette palette;
        widget->setPalette(palette);
        horizontalSlider = new QSlider(widget);
        horizontalSlider->setObjectName(QString::fromUtf8("horizontalSlider"));
        horizontalSlider->setGeometry(QRect(10, 80, 351, 22));
        horizontalSlider->setMaximum(100);
        horizontalSlider->setOrientation(Qt::Horizontal);
        textBrowser = new QTextBrowser(widget);
        textBrowser->setObjectName(QString::fromUtf8("textBrowser"));
        textBrowser->setGeometry(QRect(10, 10, 351, 31));
        progressBar_1 = new QProgressBar(widget);
        progressBar_1->setObjectName(QString::fromUtf8("progressBar_1"));
        progressBar_1->setGeometry(QRect(10, 50, 351, 23));
        progressBar_1->setValue(0);
        textBrowser_2 = new QTextBrowser(widget);
        textBrowser_2->setObjectName(QString::fromUtf8("textBrowser_2"));
        textBrowser_2->setGeometry(QRect(400, 10, 351, 31));
        progressBar_2 = new QProgressBar(widget);
        progressBar_2->setObjectName(QString::fromUtf8("progressBar_2"));
        progressBar_2->setGeometry(QRect(400, 50, 351, 23));
        progressBar_2->setMaximum(10000000);
        progressBar_2->setValue(0);
        progressBar_2->setTextVisible(true);
        horizontalSlider_2 = new QSlider(widget);
        horizontalSlider_2->setObjectName(QString::fromUtf8("horizontalSlider_2"));
        horizontalSlider_2->setGeometry(QRect(400, 80, 351, 22));
        horizontalSlider_2->setMaximum(10000000);
        horizontalSlider_2->setOrientation(Qt::Horizontal);
        pushButton = new QPushButton(widget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(950, 30, 93, 28));
        widget_2 = new QWidget(centralwidget);
        widget_2->setObjectName(QString::fromUtf8("widget_2"));
        widget_2->setGeometry(QRect(10, 680, 171, 111));
        widget_3 = new QWidget(widget_2);
        widget_3->setObjectName(QString::fromUtf8("widget_3"));
        widget_3->setGeometry(QRect(0, 10, 151, 101));
        textEdit = new QTextEdit(widget_3);
        textEdit->setObjectName(QString::fromUtf8("textEdit"));
        textEdit->setGeometry(QRect(0, 0, 71, 31));
        textEdit_2 = new QTextEdit(widget_3);
        textEdit_2->setObjectName(QString::fromUtf8("textEdit_2"));
        textEdit_2->setGeometry(QRect(0, 30, 71, 31));
        textEdit_3 = new QTextEdit(widget_3);
        textEdit_3->setObjectName(QString::fromUtf8("textEdit_3"));
        textEdit_3->setGeometry(QRect(0, 60, 71, 31));
        checkBox = new QCheckBox(widget_3);
        checkBox->setObjectName(QString::fromUtf8("checkBox"));
        checkBox->setGeometry(QRect(90, 10, 16, 20));
        checkBox_2 = new QCheckBox(widget_3);
        checkBox_2->setObjectName(QString::fromUtf8("checkBox_2"));
        checkBox_2->setGeometry(QRect(90, 70, 16, 20));
        checkBox_3 = new QCheckBox(widget_3);
        checkBox_3->setObjectName(QString::fromUtf8("checkBox_3"));
        checkBox_3->setGeometry(QRect(90, 40, 16, 20));
        openGLWidget = new QOpenGLWidget(centralwidget);
        openGLWidget->setObjectName(QString::fromUtf8("openGLWidget"));
        openGLWidget->setGeometry(QRect(180, 10, 1191, 771));
        listWidget = new QListWidget(centralwidget);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));
        listWidget->setGeometry(QRect(10, 10, 161, 651));
        MainWindow->setCentralWidget(centralwidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1375, 22));
        menuFiles = new QMenu(menuBar);
        menuFiles->setObjectName(QString::fromUtf8("menuFiles"));
        menuOpen = new QMenu(menuFiles);
        menuOpen->setObjectName(QString::fromUtf8("menuOpen"));
        menuFolder = new QMenu(menuBar);
        menuFolder->setObjectName(QString::fromUtf8("menuFolder"));
        menuMethods = new QMenu(menuFolder);
        menuMethods->setObjectName(QString::fromUtf8("menuMethods"));
        menuView_Classes = new QMenu(menuFolder);
        menuView_Classes->setObjectName(QString::fromUtf8("menuView_Classes"));
        MainWindow->setMenuBar(menuBar);

        menuBar->addAction(menuFiles->menuAction());
        menuBar->addAction(menuFolder->menuAction());
        menuFiles->addAction(menuOpen->menuAction());
        menuOpen->addAction(actionAll_Classes);
        menuOpen->addAction(actionLIDAR_DATA);
        menuFolder->addAction(menuMethods->menuAction());
        menuFolder->addAction(menuView_Classes->menuAction());
        menuMethods->addAction(actionL2_Distance);
        menuView_Classes->addAction(actionShow_Sampled_Points);
        menuView_Classes->addAction(actionShow_Bounding_Box);
        menuView_Classes->addAction(actionShow_Mesh);

        retranslateUi(MainWindow);
        QObject::connect(actionAll_Classes, SIGNAL(triggered()), MainWindow, SLOT(open_classes()));
        QObject::connect(horizontalSlider, SIGNAL(valueChanged(int)), progressBar_1, SLOT(setValue(int)));
        QObject::connect(horizontalSlider_2, SIGNAL(valueChanged(int)), progressBar_2, SLOT(setValue(int)));
        QObject::connect(toolButton, SIGNAL(clicked()), MainWindow, SLOT(get_name()));
        QObject::connect(pushButton, SIGNAL(clicked()), MainWindow, SLOT(help_button()));
        QObject::connect(actionLIDAR_DATA, SIGNAL(triggered()), MainWindow, SLOT(open_lidar()));

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        actionFiles2->setText(QCoreApplication::translate("MainWindow", "CaseStudy2", nullptr));
        actionCaseStudy3->setText(QCoreApplication::translate("MainWindow", "CaseStudy3", nullptr));
        actionCaseStudy4->setText(QCoreApplication::translate("MainWindow", "CaseStudy4", nullptr));
        actionCaseStudy5->setText(QCoreApplication::translate("MainWindow", "CaseStudy5", nullptr));
        actionCaseStudy6->setText(QCoreApplication::translate("MainWindow", "CaseStudy6", nullptr));
        actionFile1->setText(QCoreApplication::translate("MainWindow", "File1", nullptr));
        actionShow_Sampled_Points->setText(QCoreApplication::translate("MainWindow", "Show Sampled Points", nullptr));
        actionShow_Bounding_Box->setText(QCoreApplication::translate("MainWindow", "Show Bounding Box", nullptr));
        actionShow_Mesh->setText(QCoreApplication::translate("MainWindow", "Show Mesh", nullptr));
        actionL2_Distance->setText(QCoreApplication::translate("MainWindow", "L2 Distance", nullptr));
        actionCaseStudy2->setText(QCoreApplication::translate("MainWindow", "CaseStudy2", nullptr));
        actionCaseStudy3_2->setText(QCoreApplication::translate("MainWindow", "CaseStudy3", nullptr));
        actionCaseStudy4_2->setText(QCoreApplication::translate("MainWindow", "CaseStudy4", nullptr));
        actionCaseStudy5_2->setText(QCoreApplication::translate("MainWindow", "CaseStudy5", nullptr));
        actionCaseStudy6_2->setText(QCoreApplication::translate("MainWindow", "CaseStudy6", nullptr));
        actionAll_Classes->setText(QCoreApplication::translate("MainWindow", "All Classes", nullptr));
        actionLIDAR_DATA->setText(QCoreApplication::translate("MainWindow", "LIDAR DATA", nullptr));
        toolButton->setText(QCoreApplication::translate("MainWindow", "RUN", nullptr));
        textBrowser->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">Threshold</span></p></body></html>", nullptr));
        textBrowser_2->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">Density</span></p></body></html>", nullptr));
        progressBar_2->setFormat(QCoreApplication::translate("MainWindow", "%v", nullptr));
        pushButton->setText(QCoreApplication::translate("MainWindow", "TRY", nullptr));
        textEdit->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:700;\">.off</span></p></body></html>", nullptr));
        textEdit_2->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">.ply</span></p></body></html>", nullptr));
        textEdit_3->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:700;\">Point cloud</span></p></body></html>", nullptr));
        checkBox->setText(QString());
        checkBox_2->setText(QString());
        checkBox_3->setText(QString());
        menuFiles->setTitle(QCoreApplication::translate("MainWindow", "Files", nullptr));
        menuOpen->setTitle(QCoreApplication::translate("MainWindow", "Open", nullptr));
        menuFolder->setTitle(QCoreApplication::translate("MainWindow", "Options", nullptr));
        menuMethods->setTitle(QCoreApplication::translate("MainWindow", "Methods", nullptr));
        menuView_Classes->setTitle(QCoreApplication::translate("MainWindow", "View Classes", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
