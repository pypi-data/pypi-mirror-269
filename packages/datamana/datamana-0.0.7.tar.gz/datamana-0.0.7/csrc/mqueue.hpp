#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <mqueue.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;

struct MQueue {
    mqd_t mqd;

    MQueue() : mqd((mqd_t)-1) {}

    int py_mq_open(const char *name, int oflag, unsigned int mode) {
        mqd = mq_open(name, oflag, (mode_t)mode, nullptr);
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
