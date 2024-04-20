/*1
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
int main(int argc, char *argv[]) 
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int *randomNumbers = (int *)malloc(1000 * sizeof(int));
    for (int i = 0; i < 1000; i++) 
    {
        randomNumbers[i] = rand() % 1000;
    }
    int localMin = randomNumbers[0];
    for (int i = 1; i < 1000; i++) 
    {
        if (randomNumbers[i] < localMin) 
        {
            localMin = randomNumbers[i];
        }
    }
    int globalMin;
    MPI_Reduce(&localMin, &globalMin, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);
    if (rank == 0) 
    {
        printf("Minimum number: %d\n", globalMin);
    }
    free(randomNumbers);
    MPI_Finalize();
    return 0;
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
int main()
{
    int q[20],head,n,j,i,seek=0,max,diff;
    printf("\nEnter the maximum range of disk : ");
    scanf("%d",&max);
    printf("\nEnter the size of queue request : ");
    scanf("%d",&n);
    printf("\nEnter disk position to be read :\n");
    for (i=1;i<=n;i++)
        scanf("%d",&q[i]);
        printf("Enter the initial head position : ");
        scanf("%d",&head);
        q[0]=head;
        for (j=0;j<=n-1;j++)
        {
            diff=abs(q[j+1]-q[j]);
            seek+=diff;
            printf("Disk head moves from %d to %d with seek %d \n",q[j],q[j+1],diff);
        } 
        printf("Total head movement is : %d\n",seek);
        return 0;
}        
*/