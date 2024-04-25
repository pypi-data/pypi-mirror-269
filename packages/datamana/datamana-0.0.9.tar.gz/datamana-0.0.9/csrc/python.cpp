#include "semaphore.hpp"
#include "mqueue.hpp"
#include <nanobind/nanobind.h>

namespace nb = nanobind;

NB_MODULE(core, m) {
    DEFINE_SEMAPHORE_MODULE(m);
    DEFINE_MQUEUE_MODULE(m);
}
