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
        mode_t omask = umask(0);
        mqd = mq_open(name, oflag, (mode_t)mode, &attr);
        umask(omask);
        int ret = 0;
        if (mqd == (mqd_t)-1)
            ret = errno;
        return ret;
    }
    int py_mq_unlink(const char *name) {
        int ret = mq_unlink(name);
        if (ret == -1)
            ret = errno;
        return ret;
    }
    int py_mq_close() {
        int ret = mq_close(mqd);
        if (ret == -1)
            ret = errno;
        return ret;
    }
    int py_mq_send(std::string &msg, unsigned int msg_prio) {
        int ret = mq_send(mqd, (const char *)msg.c_str(), msg.size(), msg_prio);
        if (ret == -1)
            ret = errno;
        return ret;
    }
    int py_mq_receive(std::string &msg) {
        unsigned int msg_prio;
        msg.resize(attr.mq_msgsize);
        int ret = mq_receive(mqd, (char *)msg.c_str(), msg.size(), &msg_prio);
        if (ret == -1)
            ret = errno;
        return ret;
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
