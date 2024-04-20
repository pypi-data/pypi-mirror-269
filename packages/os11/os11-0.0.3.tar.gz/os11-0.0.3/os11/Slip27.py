/*1
#include <stdio.h>
#include <stdlib.h>

void sort(int requests[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (requests[j] > requests[j + 1]) {
                int temp = requests[j];
                requests[j] = requests[j + 1];
                requests[j + 1] = temp;
            }
        }
    }
}

void look(int requests[], int n, int start, int direction) {
    int total_head_movements = 0;
    int current_position;
    printf("------------Serving order------------\n");
    sort(requests, n);

    for (int i = 0; i < n; i++) {
        if (requests[i] >= start) {
            current_position = i;
            break;
        }
    }

    if (direction == -1) {
        for (int i = current_position - 1; i >= 0; i--) {
            printf("%d ", requests[i]);
            total_head_movements += abs(requests[i] - start);
            start = requests[i];
        }
    } else {
        for (int i = current_position; i < n; i++) {
            printf("%d ", requests[i]);
            total_head_movements += abs(requests[i] - start);
            start = requests[i];
        }
    }
    printf("\ntotal head movements = %d\n", total_head_movements);
}

int main() {
    int n;
    printf("Enter the total number of disk blocks: ");
    scanf("%d", &n);

    int requests[n];
    printf("Enter the disk requests: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &requests[i]);
    }

    int start;
    printf("Enter the starting head position: ");
    scanf("%d", &start);

    int direction;
    printf("Enter the direction (1 for right, -1 for left): ");
    scanf("%d", &direction);

    look(requests, n, start, direction);
    return 0;
}
*/

/*2
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