
#ifndef UTILS_H
#define UTILS_H

#include <sys/stat.h>
#include <cstring>
#include <unistd.h>
#include <fstream>
#include <iostream>
#include <dlfcn.h>
#include <libgen.h>

#include "acl/acl.h"


#define CHECK_ACL(x)                                                                        \
    do {                                                                                    \
        aclError __ret = x;                                                                 \
        if (__ret != ACL_ERROR_NONE) {                                                      \
            std::cerr << __FILE__ << ":" << __LINE__ << " aclError:" << __ret << std::endl; \
        }                                                                                   \
    } while (0);


#define EXPECT_EQ(a, b, msg) \
  do {                       \
    assert((a == b) && msg); \
  } while (0)


static char *readBinFile(const char *file_name, uint32_t *fileSize) {
  std::filebuf *pbuf;
  std::ifstream filestr;
  size_t size;
  filestr.open(file_name, std::ios::binary);
  if (!filestr) {
    std::string msg = std::string("Path of bin file does not exist. Path is ") + file_name + ".";
    throw std::runtime_error(msg);
  }
  pbuf = filestr.rdbuf();
  size = pbuf->pubseekoff(0, std::ios::end, std::ios::in);
  pbuf->pubseekpos(0, std::ios::in);
  char *buffer = new char[size];
  if (NULL == buffer) {
    return (char *)("cannot malloc buffer size");
    return NULL;
  }
  pbuf->sgetn(buffer, size);
  *fileSize = size;
  filestr.close();
  return buffer;
}


static std::string getOpsPathFromEnv() {
    const char* env_var = std::getenv("MS_INTERNAL_OPS_PATH");
    if (env_var != nullptr) {
        return std::string(env_var);
    }
    return std::string("./build/op_kernels/");
}


static bool isPathExist(const std::string& relativePath) {
    struct stat buffer;
    return (stat(relativePath.c_str(), &buffer) == 0);
}


static std::string concatOpKernelsPath(const std::string& path, const std::string& newSuffix) {
    std::string directory;
    std::string::size_type lastSlashPos = path.rfind('/');
    if (lastSlashPos != std::string::npos) {
        directory = path.substr(0, lastSlashPos + 1);
    }
    return directory + newSuffix;
}

static std::string getOpKernelsPath(void* addr) {
    Dl_info dl_info;
    if (dladdr(addr, &dl_info)) {
        auto soPath = std::string(dl_info.dli_fname);
        std::string opKernelsPath = concatOpKernelsPath(soPath, "../op_kernels");
        if (isPathExist(opKernelsPath)) {
          return opKernelsPath;
        }
        opKernelsPath = concatOpKernelsPath(soPath, "./op_kernels");
        if (isPathExist(opKernelsPath)) {
          return opKernelsPath;
        }
        return "";
    }
    return ""; // failed to retrieve the path
}

static std::string joinPaths(const std::string path1, const std::string path2) {
    if (path1.back() == '/') {
        return path1 + path2;
    }
    return path1 + "/" + path2;
}

#endif // UTILS_H