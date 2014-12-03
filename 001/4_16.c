#include <stdio.h>
#include <stdlib.h>
#include "avl.h"

void preorder(Tree T, int depth){
  if (T == NULL)
    return;
  for (int i = 0; i < depth; i++)
    putchar(' ');
  printf("%d\n", T->key);
  preorder(T->left, depth + 1);
  preorder(T->right, depth + 1);
}

int main(void){
  int node_num;
  int key;
  Tree T;

  scanf("%d", &node_num);
  scanf("%d", &key);
  T = create_tree(key);
  for (int i = 1; i < node_num; i++){
    scanf("%d", &key);
    T = insert(key, T);
  }
  preorder(T, 0);
  dispose_tree(T);

  return 0;
}
