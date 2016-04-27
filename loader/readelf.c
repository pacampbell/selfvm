#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <elf.h>
#include <sys/mman.h>
#include "readelf.h"


void* find_section(const char *fname, const char *section_name, size_t size) {
  int i, j;
  int fd = open(fname, O_RDONLY);
  char *section = NULL;
  char *program = mmap(0, size, PROT_READ, MAP_PRIVATE, fd, 0);
  // Now lets find the sections in the elf
  Elf64_Ehdr *ehdr = (Elf64_Ehdr*)program;
  Elf64_Shdr *shdr = (Elf64_Shdr*)(program + ehdr->e_shoff);

  Elf64_Shdr *sh_strtab = &shdr[ehdr->e_shstrndx];
  char *string_table = program + sh_strtab->sh_offset;

  // Start looping through the sections
  for (i = 0; i < ehdr->e_shnum; ++i) {
    // printf("%2d: %4d '%s'\n", i, shdr[i].sh_name, string_table + shdr[i].sh_name);
    // If we found the desired section, copy it
    if (strcmp(string_table + shdr[i].sh_name, section_name) == 0) {
      section = malloc(shdr[i].sh_size);
      memcpy(section, (void*)(program + shdr[i].sh_offset), shdr[i].sh_size);
      for (j = 0; j < shdr[i].sh_size; ++j) {
        fprintf(stderr, "%c", section[j]);
      }
      fprintf(stderr, "\n");
      // free(section);
    }
  }

  return section;
}
