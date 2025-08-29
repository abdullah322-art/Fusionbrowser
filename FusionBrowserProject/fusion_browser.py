import sys
import urllib.parse
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction,
                             QLineEdit, QTabWidget, QPushButton, QProgressBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fusion Browser")
        self.setWindowIcon(QIcon(self.style().standardIcon(getattr(self.style(), 'SP_ComputerIcon'))))
        self.setMinimumSize(QSize(1024, 768))

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)

        nav_toolbar = QToolBar("Navigation")
        nav_toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(nav_toolbar)

        style = self.style()
        self.back_btn = QAction(QIcon(style.standardIcon(style.SP_ArrowBack)), "Back", self)
        self.fwd_btn = QAction(QIcon(style.standardIcon(style.SP_ArrowForward)), "Forward", self)
        self.reload_btn = QAction(QIcon(style.standardIcon(style.SP_BrowserReload)), "Reload", self)
        self.stop_btn = QAction(QIcon(style.standardIcon(style.SP_BrowserStop)), "Stop", self)
        self.home_btn = QAction(QIcon(style.standardIcon(style.SP_DirHomeIcon)), "Home", self)

        self.back_btn.triggered.connect(lambda: self.active_browser().back())
        self.fwd_btn.triggered.connect(lambda: self.active_browser().forward())
        self.reload_btn.triggered.connect(lambda: self.active_browser().reload())
        self.stop_btn.triggered.connect(lambda: self.active_browser().stop())
        self.home_btn.triggered.connect(self.go_to_home)

        nav_toolbar.addActions([self.back_btn, self.fwd_btn, self.reload_btn, self.stop_btn, self.home_btn])

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        add_tab_btn = QPushButton("+")
        add_tab_btn.setFixedSize(QSize(28, 28))
        add_tab_btn.clicked.connect(lambda: self.add_new_tab(QUrl("http://127.0.0.1:5000/search")))
        nav_toolbar.addWidget(add_tab_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        nav_toolbar.addWidget(self.progress_bar)

        self.add_new_tab(QUrl("http://127.0.0.1:5000/search"), "Fusion Search")

        self.show()

    def navigate_to_url(self):
        url_text = self.url_bar.text().strip()
        if not url_text:
            return

        if '.' in url_text and ' ' not in url_text:
            if not (url_text.startswith("http://") or url_text.startswith("https://")):
                qurl = QUrl("http://" + url_text)
            else:
                qurl = QUrl(url_text)
        else:
            search_term = urllib.parse.quote_plus(url_text)
            qurl = QUrl(f"http://127.0.0.1:5000/search?q={search_term}")

        self.active_browser().setUrl(qurl)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("http://127.0.0.1:5000/search")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda q, b=browser: self.update_url_bar(q) if b == self.active_browser() else None)
        browser.loadFinished.connect(lambda _, b=browser: self.tabs.setTabText(self.tabs.indexOf(b), b.page().title()))
        browser.loadProgress.connect(
            lambda p, b=browser: self.progress_bar.setValue(p) if b == self.active_browser() else None)
        browser.loadFinished.connect(lambda b=browser: self.progress_bar.hide() if b == self.active_browser() else None)
        browser.loadStarted.connect(lambda b=browser: self.progress_bar.show() if b == self.active_browser() else None)

    def close_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)

    def active_browser(self):
        return self.tabs.currentWidget()

    def current_tab_changed(self, index):
        browser = self.active_browser()
        if browser:
            self.update_url_bar(browser.url())
            self.update_nav_buttons()

    def go_to_home(self):
        self.active_browser().setUrl(QUrl("http://127.0.0.1:5000/search"))

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)
        self.update_nav_buttons()

    def update_nav_buttons(self):
        browser = self.active_browser()
        if browser:
            self.back_btn.setEnabled(browser.page().history().canGoBack())
            self.fwd_btn.setEnabled(browser.page().history().canGoForward())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Fusion Browser")
    window = WebBrowser()
    sys.exit(app.exec_())
