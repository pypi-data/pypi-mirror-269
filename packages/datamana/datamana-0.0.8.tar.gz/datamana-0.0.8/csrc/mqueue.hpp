#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <mqueue.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;

struct MQueue {
    mqd_t mqd;
    struct mq_attr attr;

    MQueue() : mqd((mqd_t)-1) {}

    int py_mq_open(const char *name, int oflag, unsigned int mode) {
        mqd = mq_open(name, oflag, (mode_t)mode, &attr);
        if (mqd == (mqd_t)-1) {
            return errno;
        } else {
            return 0;
        }
    }
    int py_mq_unlink(const char *name) {
        return mq_unlink(name);
    }
    int py_mq_close() {
        return mq_close(mqd);
    }
    int py_mq_send(std::string &msg, unsigned int msg_prio) {
        return mq_send(mqd, (const char *)msg.c_str(), msg.size(), msg_prio);
    }
    std::string py_mq_receive() {
        unsigned int msg_prio;
        std::string msg(32, '\0');
        mq_receive(mqd, (char *)msg.c_str(), msg.size(), &msg_prio);
        return msg;
    }
};

void DEFINE_MQUEUE_MODULE(nb::module_ & (m)) {
    nb::class_<MQueue>(m, "MQueue")
        .def(nb::init<>())
        .def("open", &MQueue::py_mq_open)
        .def("close", &MQueue::py_mq_close)
        .def("unlink", &MQueue::py_mq_unlink)
        .def("send", &MQueue::py_mq_send)
        .def("receive", &MQueue::py_mq_receive)
        .def_prop_rw("maxmsg", /* Max. # of messages on queue */
            [](MQueue &mq) { return mq.attr.mq_maxmsg; },
            [](MQueue &mq, long value) { mq.attr.mq_maxmsg = value; })
        .def_prop_rw("msgsize", /* Max. message size (bytes) */
            [](MQueue &mq) { return mq.attr.mq_msgsize; },
            [](MQueue &mq, long value) { mq.attr.mq_msgsize = value; })
        .def_prop_rw("flags", /* Flags: 0 or O_NONBLOCK */
            [](MQueue &mq) { return mq.attr.mq_flags; },
            [](MQueue &mq, long value) { mq.attr.mq_flags = value; })
        .def_prop_ro("curmsgs", /* # of messages currently in queue */
            [](MQueue &mq) { return mq.attr.mq_curmsgs; });
}
