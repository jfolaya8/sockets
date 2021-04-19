#include <stdio.h>
#include <mpi.h>
int main(int argc, char *argv[]){
  int rank, size, x;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  for (x=1; x<=1000; x++){
    printf(“%d Soy el core nro. %d de %d\n”, x, rank, size);
  }
  MPI_Finalize();
  return 0;
}
