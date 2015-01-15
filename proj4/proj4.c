#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define MAX_CODE_LEN 100

typedef struct tree_record *Tree;
struct tree_record{
  int is_node;
  Tree left;
  Tree right;
};

typedef struct heap_record *Heap;
struct heap_record{
  int freq[64];
  int size;
};

Heap create_heap(void);
void dispose_heap(Heap H);
Tree create_tree(void);
void dispose_tree(Tree T);
void insert(int x, Heap H);
int sort_code_by_length(const void *code1, const void *code2);
int deletemin(Heap H);
int is_valid(char code[63][MAX_CODE_LEN], int N, int f[63], int wpl);
int get_wpl(int N, int f[63]);

int main(int argc, char *argv[]){
  int N, M;
  int i, j;
  int wpl;    // correct huffman code's wpl
  char c[63];    // store characters
  int f[63];    // store frequencies
  char code[63][MAX_CODE_LEN];    // store code

  scanf("%d", &N);
  getchar();
  for (i = 0; i < N; i++){
    c[i] = getchar();
    scanf("%d", &f[i]);
    getchar();
  }
  wpl = get_wpl(N, f);    // get the correct wpl
  scanf("%d", &M);
  getchar();
  for (i = 0; i < M; i++){
    for (j = 0; j < N; j++){
      getchar(); getchar();    // read char and space
      scanf("%s", code[j]);
    }
    if (is_valid(code, N, f, wpl))
      printf("Yes\n");
    else
      printf("No\n");
  }

  return 0;
}

// the function test if a code is valid or not
// what characters are doesn't matter
int is_valid(char code[63][MAX_CODE_LEN], int N, int f[63], int wpl){
  int i, j;
  char bit;
  int student_wpl;
  Tree T, tmpT, newT;

  student_wpl = 0;
  for (i = 0; i < N; i++){
    student_wpl += strlen(code[i]) * f[i];
  }
  if (student_wpl != wpl)    // two valid huffman codes have the same wpl
    return 0;

  // check whether there's a prefix in the huffman tree
  T = create_tree();
  // sort code by length so that longer paths appear after shorter ones
  // for the convenience of determining prefix
  // sort_code_by_length is a comparison function
  qsort(code, N, sizeof(char) * MAX_CODE_LEN, sort_code_by_length);
  for (i = 0; i < N; i++){
    tmpT = T;
    j = 0;
    while ((bit = code[i][j++])){    // read next bit until the code ends
      if (bit == '0'){    // left tree
        if (tmpT->left == NULL){
          newT = create_tree();
          tmpT->left = newT;
          tmpT = tmpT->left;
        }
        else{    // if (tmpT->left != NULL)
          if (tmpT->left->is_node){
            dispose_tree(T);
            return 0;     // there's a prefix in the left tree
          }
          tmpT = tmpT->left;
        }
      }
      else{    // right tree
        if (tmpT->right == NULL){
          newT = create_tree();
          tmpT->right = newT;
          tmpT = tmpT->right;
        }
        else{    // if (tmpT->right != NULL)
          if (tmpT->right->is_node){
            dispose_tree(T);
            return 0;    // there's a prefix in the right tree
          }
          tmpT = tmpT->right;
        }
      }
    }
    // meet the end of the code
    newT->is_node = 1;    // the final node is a single node
  }

  dispose_tree(T);
  return 1;
}

// return wpl of huffman code
int get_wpl(int N, int f[63]){
  Heap H;
  int wpl;
  int i;
  int node1, node2, merged;
  H = create_heap();
  wpl = 0;

  // insert N nodes to the heap
  for (i = 0; i < N; i++){
    insert(f[i], H);
  }
  while (H->size >= 2){
    // merge two nodes in the heap with smallest frequency
    node1 = deletemin(H);
    node2 = deletemin(H);
    merged = node1 + node2;
    insert(merged, H);
    wpl += merged;    // once inserted, wpl increases by the total number of frequencies of nodes in the path
  }
  // loop ends: H has 1 node, H[1]

  dispose_heap(H);
  return wpl;
}

// comparison function
// return value:
// a positive integer if code1 is longer than code2
// a negative integer if code1 is shorter than code2
// 0                  if code1 and code2 have the same length
int sort_code_by_length(const void *code1, const void *code2){
  return strlen(code1) - strlen(code2);
}

// Routines for heap
Heap create_heap(void){
  Heap H;
  H = (Heap)malloc(sizeof(struct heap_record));
  H->freq[0] = -1;
  H->size = 0;
  return H;
}

void dispose_heap(Heap H){
  if (H != NULL)
    free(H);
}

void insert(int x, Heap H){
  int i;
  // omit size checking
  for (i = ++H->size; H->freq[i / 2] > x; i /= 2){
    H->freq[i] = H->freq[i / 2];
  }
  H->freq[i] = x;
}

int deletemin(Heap H){
  int i, child;
  int min, last;
  min = H->freq[1];
  last = H->freq[H->size--];
  // omit size checking
  for (i = 1; i * 2 <= H->size; i = child){
    child = i * 2;
    if (child != H->size && H->freq[child + 1] < H->freq[child])
      child++;
    if (H->freq[child] < last)
      H->freq[i] = H->freq[child];
    else
      break;
  }
  H->freq[i] = last;
  return min;
}

// Routines for tree
// default is_node is False, unless manually set it True
Tree create_tree(){
  Tree T;
  T = (Tree)malloc(sizeof(struct tree_record));
  T->is_node = 0;
  T->left = T->right = NULL;
  return T;
}

// recursively free memory in a tree
void dispose_tree(Tree T){
  if (T != NULL){
    dispose_tree(T->left);
    dispose_tree(T->right);
    free(T);
  }
}
