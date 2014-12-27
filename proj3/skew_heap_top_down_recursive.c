#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define REPEAT 100
#define MAX_MERGE 1001
struct TreeNode;
typedef struct TreeNode *PriorityQueue;
PriorityQueue Merge1(PriorityQueue H1 , PriorityQueue H2);
PriorityQueue Merge(PriorityQueue H1 , PriorityQueue H2);
PriorityQueue insert(int x , PriorityQueue H);
PriorityQueue Deletemin(PriorityQueue H);
void dispose_heap(PriorityQueue H);
struct TreeNode
{
  int element;
  PriorityQueue Left;
  PriorityQueue Right;
};

PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2)
{
  if (H1 == NULL)
    return H2;
  if (H2 == NULL)
    return H1;
  if (H1->element < H2->element) 
    return Merge1(H1 , H2);
  else 
    return Merge1(H2 , H1);
}

PriorityQueue Merge1( PriorityQueue H1, PriorityQueue H2)
{
  PriorityQueue temp;

  if (H1->Left == NULL)
    H1->Left = H2;
  else
    {
      H1->Right = Merge(H1->Right, H2);
      temp = H1->Left;
      H1->Left = H1->Right;
      H1->Right = temp;
    }
  return H1;
}
PriorityQueue insert(int x, PriorityQueue H)
{
  PriorityQueue temp;
  temp =(PriorityQueue) malloc (sizeof ( struct TreeNode));
  temp->element = x;

  temp->Left = temp->Right = NULL;

  H = Merge(temp , H);
  return H;
}
 
PriorityQueue Deletemin(PriorityQueue H)
{
  PriorityQueue Leftheap, Rightheap;
  if ( H == NULL )
    {
      printf("The heap is empty\n");
      return H;
    }
  Leftheap = H->Left;
  Rightheap = H->Right;
  free (H);
  return Merge(Leftheap, Rightheap);
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

