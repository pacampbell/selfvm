#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include "readelf.h"

int main(int argc, char *argv[]) {
  void *section = NULL;
  // We want to open an instance of ourselves
  const char *fname = "/proc/self/exe";
  // Create a stat struct
  struct stat st;
  memset(&st, 0, sizeof(struct stat));
  // Check to make sure it exists
  if (stat(fname, &st) != 0) {
    perror("");
    return EXIT_FAILURE;
  }

  // Look for the section
  if ((section = find_section(fname, "sname", st.st_size)) == NULL) {
    fprintf(stderr, "Unable to locate section.\n");
    return EXIT_FAILURE;
  } else {
    fprintf(stderr, "Located the section: %s\n", "sname");
  }

  // Start translating the data

  // Since the section name is dynamically allocated in find_section - free it
  free(section);
  return EXIT_SUCCESS;
}
