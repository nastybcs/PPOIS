#include <stdio.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <errno.h>

#define BUF_SIZE 4096

void copy_file(const char *src_path, const char *dst_path) {
    int src_fd = open(src_path, O_RDONLY);
    struct stat st;
    fstat(src_fd, &st);
    int dst_fd = open(dst_path, O_WRONLY | O_CREAT | O_TRUNC, st.st_mode);

    char buf[BUF_SIZE];
    ssize_t bytes, total = 0;
    while ((bytes = read(src_fd, buf, BUF_SIZE)) > 0) {
        write(dst_fd, buf, bytes);
        total += bytes;
    }

    printf("PID %d: '%s' скопирован, байт: %ld\n", getpid(), dst_path, total);

    close(src_fd);
    close(dst_fd);
    exit(0); 
}

int main() {
    char dir1[256], dir2[256];
    
    printf("Введите первую директорию: ");
    fflush(stdout);
    fgets(dir1, sizeof(dir1), stdin);
    dir1[strcspn(dir1, "\n")] = 0;

    printf("Введите вторую директорию: ");
    fflush(stdout);
    fgets(dir2, sizeof(dir2), stdin);
    dir2[strcspn(dir2, "\n")] = 0;

    DIR *d1 = opendir(dir1);

    struct dirent *entry;
    ssize_t total_bytes_viewed = 0;

    while ((entry = readdir(d1)) != NULL) {
        if (entry->d_type != DT_REG) continue; 

        char src_path[512], dst_path[512];
        snprintf(src_path, sizeof(src_path), "%s/%s", dir1, entry->d_name);
        snprintf(dst_path, sizeof(dst_path), "%s/%s", dir2, entry->d_name);

        struct stat st;
        stat(src_path, &st);
        total_bytes_viewed += st.st_size;

        if (fork() == 0) {
            copy_file(src_path, dst_path);
        }
    }

    closedir(d1);

    while (wait(NULL) > 0);
    return 0;
}

