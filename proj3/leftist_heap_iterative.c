#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#define Size 10000
#define REPEAT 1
#define MAX_MERGE 101

struct TreeNode;
typedef struct TreeNode *PriorityQueue;
PriorityQueue Merge1(PriorityQueue H1 , PriorityQueue H2);   //merge H1 and H2
PriorityQueue Merge(PriorityQueue H1 , PriorityQueue H2);
PriorityQueue insert(int x , PriorityQueue H);    // insert x into heap H
void swap(PriorityQueue *H1, PriorityQueue *H2);   //swap H1 and H2
PriorityQueue Deletemin(PriorityQueue H);         // delete minest node in the heap H
struct TreeNode
{
  int element;
  PriorityQueue Left;  // Left child
  PriorityQueue Right;  // Right child
  int Npl;
};
PriorityQueue arr[Size];
void swap(PriorityQueue *H1, PriorityQueue *H2)
{
  PriorityQueue temp;
  temp = *H1;
  *H1 = *H2;
  *H2 = temp;
}
PriorityQueue Merge(PriorityQueue H1, PriorityQueue H2)
{
  if (H1 == NULL)
    return H2;
  if (H2 == NULL)
    return H1;
  if (H1->element < H2->element)  // make H1<H2
    return Merge1(H1 , H2);
  else
    return Merge1(H2 , H1);
}

PriorityQueue Merge1( PriorityQueue H1, PriorityQueue H2)
{
  PriorityQueue temp,x,y;

  int now;
  // x is final one after merge , y is parent of current merge tree
  x = y = H1;
  H1 = H1->Right;
  now=0;
  arr[now] = y;  //use a stack to record the merge path
  while (H1 != NULL)
    {
      if (H1->element > H2->element) //let H1 is miner one
        swap(&H1,&H2);
      y->Right = H1; //merge H1 into y
      now++;
      arr[now] = y;
      y = H1;  //next merge
      H1 = H1->Right;
    }
  y->Right = H2;
  while (now>0)
    {
      if (arr[now]->Left==NULL)  {  arr[now]->Left=arr[now]->Right; arr[now]->Right = NULL; }
      if (arr[now]->Left->Npl < arr[now]->Right->Npl) swap(&(arr[now]->Left),&(arr[now]->Right));
      arr[now]->Npl = arr[now]->Right? arr[now]->Right->Npl+1 : 0;  // calculate the Npl
      now--;
    }
  return x;
}
PriorityQueue insert(int x, PriorityQueue H)
{
  PriorityQueue temp;
  //set a new node for x;
  temp =(PriorityQueue) malloc (sizeof ( struct TreeNode));
  temp->element = x;
  temp->Npl = -1;
  temp->Left = temp->Right = NULL;
    
  H = Merge(temp , H);  //insert new node into H
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
  printf("%d ", H->element);
  free (H);   // delete the root of H
  return Merge(Leftheap, Rightheap);   // merge left subtree and right subtree of root
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
    
  fp = fopen("test1_input.txt", "r");
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



