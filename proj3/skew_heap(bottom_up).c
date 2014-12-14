#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define REPEAT 100
#define MAX_MERGE 101
struct HeapNode;
typedef struct HeapNode *PriorityQueue;

struct HeapNode
{
  PriorityQueue up;
  PriorityQueue down;
  int element;
};

PriorityQueue insert(int x, PriorityQueue H);
PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2);
void swap(PriorityQueue *H1, PriorityQueue *H2);
PriorityQueue deletemin(PriorityQueue H1);
void dispose_heap(PriorityQueue H);

void swap(PriorityQueue *H1, PriorityQueue *H2)
{
  PriorityQueue temp;
  temp = *H1;
  *H1 = *H2;
  *H2 = temp;
}
PriorityQueue insert(int x, PriorityQueue H)
{
  PriorityQueue temp;
  temp =(PriorityQueue) malloc (sizeof (struct HeapNode));
  temp->up = temp->down = temp;
  temp->element = x;
  return Merge(temp, H);
}

PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2)
{
  PriorityQueue H3,x;
  if (H1 == NULL) return H2;
  if (H2 == NULL) return H1;
  if (H1->up->element < H2->up->element) swap(&H1, &H2);
  H3 = H1->up; H1->up=H3->up; H3->up=H3;
  while (H1 != H3)
    {
      if (H1->up->element < H2->up->element) swap(&H1, &H2);
      x = H1->up; H1->up = x->up;
      x->up = x->down; x->down = H3->up; H3->up = x;
      H3 = x;
    }
  swap (&H2->up, &H3->up);
  return H2;
}

PriorityQueue Deletemin(PriorityQueue H)
{
  PriorityQueue x,y1,y2,H3;
  if (H == NULL) return NULL;
  y1 = H->up; y2 = H->down;
  if (y1->element <y2->element) swap(&y1, &y2);
  if (y1 == H) {
    free(H);
    return NULL;
  }
  H3 = y1; y1 = y1->up; H3->up = H3;
  while (1)
    {
      if (y1->element < y2->element) swap(&y1, &y2);
      if (y1 == H) 
        {
          free(H);
          return H3;
        }
      x = y1; y1= y1->up;
      x->up = x->down; x->down = H3->up; H3->up = x;
      H3 = x;
    }
}

void dispose_heap(PriorityQueue H){
  while (H != NULL)
    H = Deletemin(H);
}

int main(int argc, char const *argv[])
{
  PriorityQueue H[REPEAT][MAX_MERGE];
  FILE * fp;
  int size;    /* size of the merged heap */
  int merges;    /* time of merges */
  int each_size;
  int i, x;
  int rpt;    /* repeat count */
  int merge_cnt;    /* merge count */
  /* merge(H[rpt][0], H[rpt][1]), merge(H[rpt][1], H[rpt][2]), ... */
  clock_t start, stop;
  double duration;

  /* set all heaps to NULL */
  memset(H, 0, sizeof(PriorityQueue) * REPEAT * MAX_MERGE);

  fp = fopen("settings.txt", "r");
  fscanf(fp, "%d%d", &size, &merges);
  fclose(fp);
  each_size = size / merges;

  fp = fopen("test_cases/test_all.txt", "r");
  for (merge_cnt = 0; merge_cnt < merges; merge_cnt++){
    for (i = 0; i < each_size; i++){
      fscanf(fp, "%d", &x);
      for (rpt = 0; rpt < REPEAT; rpt++)
        H[rpt][merge_cnt] = insert(x, H[rpt][merge_cnt]);
    }
  }
  fclose(fp);
  /* finish input */

  start = clock();

  for (merge_cnt = 0; merge_cnt < merges - 1; merge_cnt++)
    for (rpt = 0; rpt < REPEAT; rpt++)
      H[rpt][merge_cnt + 1] = Merge(H[rpt][merge_cnt], H[rpt][merge_cnt + 1]);

  stop = clock();

  duration = (double)(stop - start) / CLOCKS_PER_SEC;
  printf("%lf\n", duration);    /* print the 1st merge time */

  return 0;
}
