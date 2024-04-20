/*
#include<stdio.h>
int main() 
{    
    int n, m, i, j, k;
    printf("Enter the number of processes: ");
    scanf("%d", &n);
    printf("Enter the number of resources: ");
    scanf("%d", &m);

    int allocation[n][m], max[n][m], need[n][m];
    int available[m], safe_sequence[n], finish[n];    
    printf("Enter the allocation matrix:\n");
    for (i = 0; i < n; i++) 
    {
        for (j = 0; j < m; j++) 
        {
          scanf("%d", &allocation[i][j]);
        }
    }
    printf("Enter the maximum matrix:\n");
    for (i = 0; i < n; i++) 
    {
        for (j = 0; j < m; j++) 
        {
          scanf("%d",&max[i][j]);
        }
    }
    printf("\nNeed :");
    for (i = 0; i < n; i++) 
    {
        printf("\n p%d \t",i);
        for (j = 0; j < m; j++) 
        {
            need[i][j] = max[i][j] - allocation[i][j];
            printf("%d\t ",need[i][j]);
        }
    }
    printf("\nEnter the available resources vector:\n");
    for (i = 0; i < m; i++) 
    {
        scanf("%d", &available[i]);
    }
    for (i = 0; i < n; i++) 
    {
        finish[i] = 0;
    }
    int count = 0;
    while (count < n) 
    {
        int found = 0;
        for (i = 0; i < n; i++) 
        {
            if (finish[i] == 0) 
            {
                int safe = 1;
                for (j = 0; j < m; j++) 
                {
                    if (need[i][j] > available[j]) 
                    {
                        safe = 0;
                        break;
                    }
                }
               if (safe == 1) 
               {
                    safe_sequence[count] = i;
                    count++;
                    finish[i] = 1;
                    found = 1;
                    for (j = 0; j < m; j++) 
                    {
                        available[j] += allocation[i][j];
                    }
               }
            }
        }
        if (found == 0) 
        {
          printf("System is in unsafe state.\n");
          return 0;
        }
    }
     printf("Safe sequence is: ");
     for (i = 0; i < n; i++) 
     {
        printf("%d ", safe_sequence[i]);
     }
     printf("\n");
     return 0;
}
*/


/*
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