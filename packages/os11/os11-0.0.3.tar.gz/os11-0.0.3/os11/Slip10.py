/*1
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
        local_numbers[i] = rand();
    }

    int local_sum = 0;
    for (int i = 0; i < elements_per_process; i++) 
    {
        local_sum += local_numbers[i];
    }
    int all_sums[size];
    MPI_Gather(&local_sum, 1, MPI_INT, all_sums, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int total_sum = 0;
    if (rank == 0) 
    {
        for (int i = 0; i < size; i++) 
        {
            total_sum += all_sums[i];
        }
    }
    double global_average;
    if (rank == 0) 
    {
        global_average = (double)total_sum / 1000;
    }
    if (rank == 0) 
    {
        printf("Total Sum: %d\n", total_sum);
        printf("Global Average: %.2f\n", global_average);
    }
    MPI_Finalize();
    return 0;
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
int main()
{
	int i,j,n,seek=0,max,head,move,q[100];
	printf("\n Enter queue size:");
	scanf("%d",&n);
	printf("\n Enter queue elements:");
	for(i=0;i<n;i++)
		scanf("%d",&q[i]);
	printf("\n Enter initial head position:");
	scanf("%d",&head);
	printf("\n Enter max disk size:");
	scanf("%d",&max);
	printf("\n Enter the head movemnet direction 1 for high and 0 foe low:");
	scanf("%d",&move);
	
	for(i=0;i<n;i++)
	{
	    for(j=0;j<n-i-1;j++)
	    {
		if(q[j]>q[j+1])
		{
		     int temp;
		     temp=q[j];
		     q[j]=q[j+1];
		     q[j+1]=temp;
		}
	    }
	}
	int index;
	for(i=0;i<n;i++)
	{
	   if(head<q[i])
	   {
		index=i;
		break;
	   }
	}
	printf("\n Sequence of head movement:");
	if(move==1)
	{
		printf("%d\t",head);
		for(i=index;i<n;i++)
		{
		  seek+=abs(q[i]-head);
		  head=q[i];
		  printf("%d\t",q[i]);
		}
		seek+=abs(max-q[i-1]-1);
		seek+=abs(max-1-0);
		printf("%d\t",max-1);
		head=0;
		printf("%d\t",head);
		for(i=0;i<index;i++)
		{
		    seek+=abs(q[i]-head);
		    head=q[i];
	            printf("%d\t",q[i]);
		}
	}
	else
	{
		printf("%d\t",head);
		for(i=index-1;i>=0;i--)
		{
		   seek+=abs(q[i]-head);
		   head=q[i];
		   printf("%d\t",q[i]);
		}
		seek+=abs(q[i+1]-0);
		seek+=abs(max-1-0);
		head=max-1;
		printf("%d\t",head);
		for(i=n-1;i>=index;i--)
		{
		   seek+=abs(q[i]-head);
		   head=q[i];
		   printf("%d\t",q[i]);
		}
	}
	printf("\n\n Total head movements are %d",seek);
	return 0;
}
*/