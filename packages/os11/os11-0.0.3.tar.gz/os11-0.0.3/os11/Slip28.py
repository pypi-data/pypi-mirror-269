
/*1
#include <stdio.h>
#include <stdlib.h>

void sort(int request[], int n)
{
    int i, j;
    for (i = 0; i < n - 1; i++)
    {
        for (j = 0; j < n - i - 1; j++)
        {
            if (request[j] > request[j + 1])
            {
                int temp = request[j];
                request[j] = request[j + 1];
                request[j + 1] = temp;
            }
        }
    }
}

void clook(int request[], int n, int start, int direction)
{
    int total_head_movements = 0;
    int i;
    printf("------------Serving order------------\n");
    sort(request, n); 
    int current_position;
 
    for (i = 0; i < n; i++)
    {
        if (request[i] >= start)
        {
            current_position = i;
            break;
        }
    }
    if (direction == 1) 
    {
        for (i = current_position; i < n; i++)
        {
            printf("%d ", request[i]);
            total_head_movements += abs(request[i] - start);
            start = request[i];
        }

        for (i = 0; i <= current_position - 1; i++)
        {
            printf("%d ", request[i]);
            total_head_movements += abs(request[i] - start);
            start = request[i];
        }
    }
    else
    {
        for (i = current_position - 1; i >= 0; i--)
        {
            printf("%d ", request[i]);
            total_head_movements += abs(request[i] - start);
            start = request[i];
        }
        for (i = n - 1; i >= current_position; i--)
        {
            printf("%d ", request[i]);
            total_head_movements += abs(request[i] - start);
            start = request[i];
        }
    }
    printf("\ntotal head movements = %d\n", total_head_movements);
}

int main()
{
    int request[100], total_head_movements = 0;
    int i, n, start, direction;
    printf("enter the total number of disk blocks = \n");
    scanf("%d", &n);
    printf("enter the disk request = \n");
    for (i = 0; i < n; i++)
    {
        scanf("%d", &request[i]);
    }
    printf("enter the starting head position = \n");
    scanf("%d", &start);
    printf("enter the direction (1 for right, -1 for left)\n");
    scanf("%d", &direction);
    clook(request, n, start, direction);
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
        local_numbers[i] = rand();
    }

    int local_odd_sum = 0;
    for (int i = 0; i < elements_per_process; i++) 
    {
        if (local_numbers[i] % 2 != 0)
        {
            local_odd_sum += local_numbers[i];
        }
    }
    int all_odd_sums[size];
    MPI_Gather(&local_odd_sum, 1, MPI_INT, all_odd_sums, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int total_odd_sum = 0;
    if (rank == 0) {
        for (int i = 0; i < size; i++) 
        {
            total_odd_sum += all_odd_sums[i];
        }
    }
    if (rank == 0) 
    {
        printf("Total Sum of Odd Numbers: %d\n", total_odd_sum);
    }
    MPI_Finalize();
    return 0;
}
*/