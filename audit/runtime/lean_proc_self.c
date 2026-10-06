#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
ssize_t readlink(const char *path, char *buf, size_t n) {
    static ssize_t (*original)(const char *, char *, size_t);
    if (!original) original = dlsym(RTLD_NEXT, "readlink");
    char own[64];
    snprintf(own, sizeof(own), "/proc/%ld/exe", (long)getpid());
    return original(strcmp(path, own) == 0 ? "/proc/self/exe" : path, buf, n);
}
