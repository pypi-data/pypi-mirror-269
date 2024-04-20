#include "semaphore.hpp"
#include "mqueue.hpp"
#include <nanobind/nanobind.h>

namespace nb = nanobind;

NB_MODULE(core, m) {
    nb::class_<Semaphore>(m, "Semaphore")
        .def(nb::init<>())
        .def("open", &Semaphore::py_sem_open)
        .def("close", &Semaphore::py_sem_close)
        .def("unlink", &Semaphore::py_sem_unlink)
        .def("wait", &Semaphore::py_sem_wait)
        .def("post", &Semaphore::py_sem_post);

    nb::class_<MQueue>(m, "MQueue")
        .def(nb::init<>())
        .def("open", &MQueue::py_mq_open)
        .def("close", &MQueue::py_mq_close)
        .def("unlink", &MQueue::py_mq_unlink)
        .def("send", &MQueue::py_mq_send)
        .def("receive", &MQueue::py_mq_receive);
}
