#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0
#define get_height(T) (((T) == NULL) ? 0 : ((T)->height))
#define get_balance(T) (((T) == NULL) ? 0 : (get_height((T)->left) - get_height((T)->right)))

typedef struct node *Tree;
struct node{
  int key;
  Tree left;
  Tree right;
  int height;
};

Tree create_tree(int key);
void dispose_tree(Tree T);
int max(int a, int b);
Tree right_rotation(Tree T);
Tree left_rotation(Tree T);
Tree lr_rotation(Tree T);
Tree rl_rotation(Tree T);
Tree insert(int key, Tree T);

Tree create_tree(int key){
  Tree T;

  T = (Tree)malloc(sizeof(struct node));
  T->left = T->right = NULL;
  T->key = key;
  T->height = 1;

  return T;
}

void dispose_tree(Tree T){
  /* recursively dispose a tree */
  if (T->left != NULL)
    dispose_tree(T->left);
  if (T->right != NULL)
    dispose_tree(T->right);
  free(T);
}

int max(int a, int b){
  if (a > b)
    return a;
  else
    return b;
}

Tree right_rotation(Tree T){
  /* a -> b -> c => a <- b -> c */
  Tree right_child;

  right_child = T->right;

  T->height = max(get_height(T->left), get_height(right_child->left)) + 1;
  right_child->height = max(get_height(T), get_height(right_child->right)) + 1;

  T->right = right_child->left;
  right_child->left = T;

  return right_child;
}

Tree left_rotation(Tree T){
  /* a <- b <- c => a <- b -> c */
  Tree left_child;

  left_child = T->left;

  T->height = max(get_height(left_child->right), get_height(T->right)) + 1;
  left_child->height =  max(get_height(left_child->left), get_height(T)) + 1;

  T->left = left_child->right;
  left_child->right = T;

  return left_child;
}

Tree lr_rotation(Tree T){
  Tree child, grandchild;

  child = T->left;
  grandchild = child->right;

  child->height = max(get_height(child->left), get_height(grandchild->left)) + 1;
  T->height = max(get_height(T->right), get_height(grandchild->right)) + 1;
  grandchild->height = max(child->height, T->height) + 1;

  child->right = grandchild->left;
  T->left = grandchild->right;
  grandchild->left = child;
  grandchild->right = T;

  return grandchild;
}

Tree rl_rotation(Tree T){
  Tree child, grandchild;

  child = T->right;
  grandchild = child->left;

  child->height = max(get_height(child->right), get_height(grandchild->right)) + 1;
  T->height = max(get_height(T->left), get_height(grandchild->left)) + 1;
  grandchild->height = max(child->height, T->height) + 1;

  child->left = grandchild->right;
  T->right = grandchild->left;
  grandchild->left = T;
  grandchild->right = child;

  return grandchild;
}

Tree insert(int key, Tree T){
  int balance_factor;
  if (T == NULL)
    return create_tree(key);

  if (key > T->key)
    T->right = insert(key, T->right);
  else
    T->left = insert(key, T->left);

  T->height = max(get_height(T->left), get_height(T->right)) + 1;

  balance_factor = get_balance(T);
  if (balance_factor > 1 && key < T->left->key)    /* LL insertion */
    return left_rotation(T);
  if (balance_factor < -1 && key > T->right->key)    /* RR insertion */
    return right_rotation(T);
  if (balance_factor > 1 && key > T->left->key)    /* LR insertion */
    return lr_rotation(T);
  if (balance_factor < -1 && key < T->right->key)    /* RL insertion */
    return rl_rotation(T);

  return T;
}
