#include <mpi.h>
#include <stdio.h>

int main (argc, argv)
     int argc;
     char *argv[];
{
  int rank,size;
  char cmd[1000];
  MPI_Init (&argc, &argv);	/* starts MPI */
  MPI_Comm_rank (MPI_COMM_WORLD, &rank);	/* get current process id */
  MPI_Comm_size (MPI_COMM_WORLD, &size);	/* get number of processes */
  sprintf(cmd,"%s %d %d",argv[1],rank,size);
  system(cmd);
  MPI_Finalize();
  return 0;
}


