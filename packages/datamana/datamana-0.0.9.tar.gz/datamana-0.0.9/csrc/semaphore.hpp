#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <semaphore.h>
#include <nanobind/nanobind.h>

namespace nb = nanobind;

struct Semaphore {
    sem_t *sem;

    Semaphore() : sem((sem_t *)0) {}

    int py_sem_open(const char *name, int oflag, unsigned int mode, unsigned int value) {
        sem = sem_open(name, oflag, (mode_t)mode, value);
        if (sem == (sem_t *)SEM_FAILED) {
            sem = 0;
            return errno;
        } else {
            return 0;
        }
    }
    int py_sem_unlink(const char *name) {
        return sem_unlink(name);
    }
    int py_sem_close() {
        return sem_close(sem);
    }
    int py_sem_post() {
        return sem_post(sem);
    }
    int py_sem_wait() {
        return sem_wait(sem);
    }
};

void DEFINE_SEMAPHORE_MODULE(nb::module_ & (m)) {
    nb::class_<Semaphore>(m, "Semaphore")
        .def(nb::init<>())
        .def("open", &Semaphore::py_sem_open)
        .def("close", &Semaphore::py_sem_close)
        .def("unlink", &Semaphore::py_sem_unlink)
        .def("wait", &Semaphore::py_sem_wait)
        .def("post", &Semaphore::py_sem_post);
}
