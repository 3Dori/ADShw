#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define abs(x) ({                               \
      int _x = x;                               \
      _x > 0? _x: -_x;})

typedef int *set;

void turnpike(set D);
void _turnpike(set D, int left, int right);
int delete_max(set S, int size);
int find_max(set S, int size);
set copy(set S, int size);
int delete(int X, set S, int size);

int N;
int d_size;
int *X;

int main(void){
  set D;

  scanf("%d", &N);
  X = (int *)malloc(sizeof(int) * (N + 1));
  d_size = N * (N - 1) / 2;
  D = (set)malloc(sizeof(int) * d_size);
  for (int i = 0; i < d_size; i++)
    scanf("%d", &D[i]);

  turnpike(D);

  free(X);
  free(D);
  return 0;
}

void turnpike(set D){
  X[1] = 0;
  X[N] = delete_max(D, d_size);
  _turnpike(D, 1, N);
}

void _turnpike(set D, int left, int right){
  // X can be reused since left and right is given
  // D is copied in each recursion for efficiency
  set Dl, Dr;
  int D_max;

  if (left + 1 >= right){
    // recursion ends
    for (int i = 1; i <= N; i++)
      printf("%d ", X[i]);
    printf("\n");
    return;
  }

  D_max = find_max(D, d_size);

  // place D_max at right
  Dr = copy(D, d_size);
  for (int i = 1; i <= left; i++)
    if (!delete(abs(X[i] - D_max), Dr, d_size)){
      // not found and delete, can't place
      free(Dr);
      goto LEFT;
    }
  for (int i = right; i <= N; i++)
    if (!delete(abs(X[i] - D_max), Dr, d_size)){
      free(Dr);
      goto LEFT;
    }
  // successfully delete distance, go on into next recursion
  X[right - 1] = D_max;
  _turnpike(Dr, left, right - 1);
  free(Dr);

 LEFT:
  // place D_max at left
  Dl = copy(D, d_size);
  for (int i = 1; i <= left; i++)
    if (!delete(abs(X[N] - D_max - X[i]), Dl, d_size)){
      free(Dl);
      goto END;
    }
  for (int i = right; i <= N; i++)
    if (!delete(abs(X[N] - D_max - X[i]), Dl, d_size)){
      free(Dl);
      goto END;
    }
  X[left + 1] = X[N] - D_max;
  _turnpike(Dl, left + 1, right);
  free(Dl);

 END:;
}

set copy(set S, int size){
  set T;
  T = (set)malloc(sizeof(int) * size);
  memcpy(T, S, sizeof(int) * size);
  return T;
}

int find_max(set S, int size){
  int max;
  max = S[0];
  for (int i = 0; i < size; i++)
    if (S[i] > 0 && S[i] > max)
      max = S[i];

  return max;
}

int delete(int x, set S, int size){
  for (int i = 0; i < size; i++)
    if (S[i] == x){
      S[i] = 0;
      return 1;
    }

  return 0;
}

int delete_max(set S, int size){
  int max;
  int index;

  max = S[0];
  index = 0;
  for (int i = 0; i < size; i++)
    if (S[i] > 0 && S[i] > max){
      max = S[i];
      index = i;
    }

  S[index] = 0;    // set as deleted
  return max;
}
