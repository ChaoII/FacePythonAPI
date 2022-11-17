#include "src/utils/utils.h"

FRLogger::FRLogger(bool verbose, const std::string &prefix) {
    verbose_ = verbose;
    line_ = "";
    prefix_ = prefix;
}

FRLogger &FRLogger::operator<<(std::ostream &(*os)(std::ostream &)) {
    if (!verbose_) {
        return *this;
    }
    std::cout << prefix_ << " " << line_ << std::endl;
    line_ = "";
    return *this;
}
