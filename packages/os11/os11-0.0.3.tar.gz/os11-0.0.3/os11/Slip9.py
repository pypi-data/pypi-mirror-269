/*1
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

/*2
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