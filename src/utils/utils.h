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
class FACEAPI FRLogger {
public:
    FRLogger() {
        line_ = "";
        prefix_ = "[FR]";
        verbose_ = true;
    }

    explicit FRLogger(bool verbose, const std::string &prefix = "[FR]");

    template<typename T>
    FRLogger &operator<<(const T &val) {
        if (!verbose_) {
            return *this;
        }
        std::stringstream ss;
        ss << val;
        line_ += ss.str();
        return *this;
    }

    FRLogger &operator<<(std::ostream &(*os)(std::ostream &));

    ~FRLogger() {
        if (!verbose_ && line_ != "") {
            std::cout << line_ << std::endl;
        }
    }

private:
    std::string line_;
    std::string prefix_;
    bool verbose_ = true;
};


#define FRERROR                                                \
  FRLogger(true, "[ERROR]") << __FILE__ << "(" << __LINE__ \
                            << ")::" << __FUNCTION__ << "\t"

#define FRWARNING                                                \
  FRLogger(true, "[WARNING]") << __FILE__ << "(" << __LINE__ \
                              << ")::" << __FUNCTION__ << "\t"

#define FRINFO                                                \
  FRLogger(true, "[INFO]") << __FILE__ << "(" << __LINE__ \
                           << ")::" << __FUNCTION__ << "\t"

#define RRASSERT(condition, format, ...)                        \
  if (!(condition)) {                                           \
    int n = std::snprintf(nullptr, 0, format, ##__VA_ARGS__);   \
    std::vector<char> buffer(n + 1);                            \
    std::snprintf(buffer.data(), n + 1, format, ##__VA_ARGS__); \
    FDERROR << buffer.data() << std::endl;                      \
    std::abort();                                               \
  }

