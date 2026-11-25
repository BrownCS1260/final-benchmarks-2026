#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <time.h>

extern uint64_t lisp_entry(void *heap);

#define num_mask   0b11
#define num_tag    0b00
#define num_shift  2

#define bool_mask  0b1111111
#define bool_tag   0b0011111
#define bool_shift 7

#define heap_mask 0b111
#define pair_tag 0b010

#define nil_tag 0b11111111

void print_value(uint64_t value) {
  if ((value & num_mask) == num_tag) {
    int64_t ivalue = (int64_t)value;
    printf("%" PRIi64, ivalue >> num_shift);
  } else if ((value & bool_mask) == bool_tag) {
    if (value >> bool_shift) {
      printf("true");
    }
    else {
      printf("false");
    }
  } else if ((value & heap_mask) == pair_tag) {
    uint64_t v1 = *(uint64_t *)(value - pair_tag);
    uint64_t v2 = *(uint64_t *)(value - pair_tag + 8);
    printf("(pair ");
    print_value(v1);
    printf(" ");
    print_value(v2);
    printf(")");
  } else if (value == nil_tag) {
    printf("()");
  } else {
    printf("BAD VALUE: %" PRIu64, value);
  }
}

void lisp_error(char *exp) {
  printf("Stuck[%s]", exp);
  exit(1);
}

int main(int argc, char **argv) {
  void *heap = malloc(4096);
  struct timespec start, end;
  clock_gettime(CLOCK_MONOTONIC, &start);
  uint64_t result = lisp_entry(heap);
  clock_gettime(CLOCK_MONOTONIC, &end);
  long elapsed = (end.tv_sec - start.tv_sec) * 1000000000L
               + (end.tv_nsec - start.tv_nsec);
  print_value(result);
  printf("\n");
  fprintf(stderr, "TIME_NS:%ld\n", elapsed);
  return 0;
}

uint64_t read_num() {
  int r;
  scanf("%d", &r);
  return (uint64_t)(r) << num_shift;
}

void print_newline() {
  printf("\n");
}
