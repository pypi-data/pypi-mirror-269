"""Contains class for executing a long running process (LRP) in a separate
process, while showing a progress bar"""

import multiprocessing as mp

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets


class ProgressDialog(QtWidgets.QDialog):
    """Dialog which performs a operation in a separate process, shows a
    progress bar, and returns the result of the operation

    Parameters
    ----
    title: str
        Title of the dialog
    operation: callable
        Function of the form f(conn, *args) that will be run
    args: tuple
        Additional arguments for operation
    parent: QWidget
        Parent widget

    Returns
    ----
    result: int
        The result is an integer. A 0 represents successful completion, or
        cancellation by the user. Negative numbers represent errors. -999
        is reserved for any unforeseen uncaught error in the operation.

    Examples
    ----
    The function passed as the operation parameter should be of the form
    ``f(conn, *args)``. The conn argument is a Connection object, used to
    communicate the progress of the operation to the GUI process. The
    operation can pass its progress with a number between 0 and 100, using
    ``conn.send(i)``. Once the process is finished, it should send 101.
    Error handling is done by passing negative numbers.

    >>> def some_function(conn, *args):
    >>>     conn.send(0)
    >>>     a = 0
    >>>     try:
    >>>         for i in range(100):
    >>>                 a += 1
    >>>                 conn.send(i + 1)  # Send progress
    >>>     except Exception:
    >>>         conn.send(-1)  # Send error code
    >>>     else:
    >>>         conn.send(101)  # Send successful completion code

    Now we can use an instance of the ProgressDialog class within any
    QtWidget to execute the operation in a separate process, show a progress
    bar, and print the error code:

    >>> progress_dialog = ProgressDialog("Running...", some_function, self)
    >>> progress_dialog.finished.connect(lambda err_code: print(err_code))
    >>> progress_dialog.open()
    """

    def __init__(self, title, operation, args=(), parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint)
        self.setWindowTitle(title)
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setValue(0)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # Create connection pipeline
        self.parent_conn, self.child_conn = mp.Pipe()

        # Create process
        args = (self.child_conn, *args)
        self.process = mp.Process(target=operation, args=args)

        # Create status emitter
        self.progress_emitter = ProgressEmitter(self.parent_conn, self.process)
        self.progress_emitter.signals.progress.connect(self.slot_update_progress)
        self.thread_pool = QtCore.QThreadPool()

    def slot_update_progress(self, i):
        if i < 0:
            self.done(i)
        elif i == 101:
            self.done(0)
        else:
            self.progress_bar.setValue(i)

    def open(self):
        super().open()
        self.process.start()
        self.thread_pool.start(self.progress_emitter)

    def closeEvent(self, *args):
        self.progress_emitter.running = False
        self.process.terminate()
        super().closeEvent(*args)


class ProgressEmitter(QtCore.QRunnable):
    """Listens to status of process"""

    class ProgressSignals(QtCore.QObject):
        progress = QtCore.pyqtSignal(int)

    def __init__(self, conn, process):
        super().__init__()
        self.conn = conn
        self.process = process
        self.signals = ProgressEmitter.ProgressSignals()
        self.running = True

    def run(self):
        while self.running:
            if self.conn.poll():
                progress = self.conn.recv()
                self.signals.progress.emit(progress)
                if progress < 0 or progress == 101:
                    self.running = False
            elif not self.process.is_alive():
                self.signals.progress.emit(-999)
                self.running = False


def some_function(conn, *args):
    conn.send(0)
    a = 0
    try:
        for i in range(100):
            a += 1
            conn.send(i + 1)  # Send progress
    except Exception:
        conn.send(-1)  # Send error code
    else:
        conn.send(101)  # Send successful completion code


def main():
    progress_dialog = ProgressDialog("Running...", some_function)
    # progress_dialog.finished.connect(lambda err_code: print(err_code))
    progress_dialog.open()


if __name__ == "__main__":
    main()
