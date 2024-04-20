/*1
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

/*2
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
int main(int argc, char *argv[]) 
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int elements_per_process = 1000 / size;
    srand(rank);   
    
    int local_numbers[elements_per_process];
    for (int i = 0; i < elements_per_process; i++)
    {
        local_numbers[i] = rand()%1000;
    }

    int local_even_sum = 0;
    for (int i = 0; i < elements_per_process; i++) 
    {
        if (local_numbers[i] % 2 == 0) 
        {
            local_even_sum += local_numbers[i];
        }
    }
    int all_even_sums[size];
    MPI_Gather(&local_even_sum, 1, MPI_INT, all_even_sums, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int total_even_sum = 0;
    if (rank == 0)
    {
        for (int i=0;i<size;i++) 
        {
           total_even_sum += all_even_sums[i];
        }
    }
    if (rank == 0)
    {
        printf("Total Sum of Even Numbers: %d\n", total_even_sum);
    }
    MPI_Finalize();
    return 0;
*/