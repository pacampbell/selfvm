#ifndef READELF_H
#define READELF_H
#include <stdlib.h>

void* find_section(const char *fname, const char *section_name, size_t size);

#endif
