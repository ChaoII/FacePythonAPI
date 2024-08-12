#pragma once

#include <iostream>
#include <sstream>

#if defined(_WIN32)
#ifdef FACE_LIB
#define FACEAPI __declspec(dllexport)
#else
#define FACEAPI __declspec(dllimport)
#endif  // FACE_LIB
#else
#define FACEAPI __attribute__((visibility("default")))
#endif  // _WIN32


#ifdef _WIN32

#define __FILENAME__ (strrchr(__FILE__,'\\')?(strrchr(__FILE__,'\\')+1):__FILE__)
#else
#define __FILENAME__ (strrchr(__FILE__,'/')?(strrchr(__FILE__,'/')+1):__FILE__)
#endif //_WIN32

#ifdef USE_SPDLOG

#include <spdlog/spdlog.h>

#endif
enum LOG_LEVEL {
    LOG_DEBUG,
    LOG_INFO,
    LOG_WARNING,
    LOG_ERROR
};

class FACEAPI FRLogger {
public:
    FRLogger() {
        line_ = "";
        prefix_ = "[FR]";
        log_level_ = LOG_LEVEL::LOG_INFO;
    }

    explicit FRLogger(LOG_LEVEL log_level, const std::string &prefix = "[FR]",
                      LOG_LEVEL activate_level = LOG_LEVEL::LOG_INFO);

    template<typename T>
    FRLogger &operator<<(const T &val) {
        if (log_level_ < activate_level_) {
            return *this;
        }
        std::stringstream ss;
        ss << val;
        line_ += ss.str();
        return *this;
    }

    FRLogger &operator<<(std::ostream &(*os)(std::ostream &));

    ~FRLogger() {

    }

private:
    std::string line_;
    std::string prefix_;
    LOG_LEVEL log_level_;
    LOG_LEVEL activate_level_;
};


#define FRERROR                                                \
  FRLogger(LOG_LEVEL::LOG_ERROR, "[ERROR]") << __FILENAME__ << "(" << __LINE__ \
                            << ")::" << __FUNCTION__ << "\t|"

#define FRWARNING                                                \
  FRLogger(LOG_LEVEL::LOG_WARNING,"[WARNING]") << __FILENAME__ << "(" << __LINE__ \
                              << ")::" << __FUNCTION__ << "\t|"

#define FRINFO                                                \
  FRLogger(LOG_LEVEL::LOG_INFO,"[INFO]") << __FILENAME__ << "(" << __LINE__ \
                           << ")::" << __FUNCTION__ << "\t|"

#define FRDEBUG                                                \
  FRLogger(true, LOG_LEVEL::LOG_DEBUG,"[DEBUG]") << __FILENAME__ << "(" << __LINE__ \
                           << ")::" << __FUNCTION__ << "\t|"

#define RRASSERT(condition, format, ...)                        \
  if (!(condition)) {                                           \
    int n = std::snprintf(nullptr, 0, format, ##__VA_ARGS__);   \
    std::vector<char> buffer(n + 1);                            \
    std::snprintf(buffer.data(), n + 1, format, ##__VA_ARGS__); \
    FDERROR << buffer.data() << std::endl;                      \
    std::abort();                                               \
  }