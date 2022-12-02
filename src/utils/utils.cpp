#include "src/utils/utils.h"

FRLogger::FRLogger(LOG_LEVEL log_level, const std::string &prefix, LOG_LEVEL activate_level) {
#ifdef USE_SPDLOG
    spdlog::set_pattern("%Y-%m-%d %H:%M:%S.%e%$%^ | %l | %$%v");
#endif
    line_ = "";
    prefix_ = prefix;
    log_level_ = log_level;
    activate_level_ = activate_level;
}

FRLogger &FRLogger::operator<<(std::ostream &(*os)(std::ostream &)) {
    if (log_level_ < activate_level_) {
        return *this;
    }
#ifdef USE_SPDLOG
    switch (log_level_) {
        case LOG_LEVEL::DEBUG: {
            SPDLOG_DEBUG(line_);
            break;
        }
        case LOG_LEVEL::INFO: {
            SPDLOG_INFO(line_);
            break;
        }
        case LOG_LEVEL::WARNING: {
            SPDLOG_WARN(line_);
            break;
        }
        case LOG_LEVEL::ERROR: {
            SPDLOG_ERROR(line_);
            break;
        }
        default: {
            SPDLOG_INFO(line_);
        }
    }
#else
    std::cout << prefix_ << line_ << std::endl;
#endif
    line_ = "";
    return *this;
}
