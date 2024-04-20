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


/*2
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int bv[50],i,st,j,len,c,k;
char name[10][30];
int start[10],length[10],num=0;
void displayBitVector()
{
     printf("\nBit Vector contents :\n");
     for (i=0;i<50;i++)
          printf("%d ",bv[i]);
}
void createFile()
{
     char temp[30];
     printf("Enter the name of file : ");
     scanf("%s",&temp);
     for (int i=0;i<num;i++)
          if (strcmp(name[i],temp)==0)
          {
              printf("\nFilename already exists");
              return;
          } 
     strcpy(name[num],temp);
     printf("Enter the start block of the file : ");
     scanf("%d",&start[num]);
     printf("Enter the length of the file : ");
     scanf("%d",&length[num]);
     
     for (j=start[num];j<(start[num]+length[num]);j++)
          if (bv[j]==0)
          {
              printf("File cannot be allocated.... block already allocated");
              strcpy(name[j],"-");
              start[j]=0;
              length[j]=0;
              return;
          }
     for (j=start[num];j<(start[num]+length[num]);j++)
     {
          bv[j]=0;
          printf("\n%d->%d",j,bv[j]);
     }
     num++;
}
void deleteFile()
{
     char temp[10];
     printf("\nEnter the filename : ");
     scanf("%s",&temp);
     for (int i=0;i<num;i++)
     {
          if (strcmp(name[i],temp)==0)
          {
             
            for (j=start[i];j<(start[i]+length[i]);j++)
            {
              bv[j]=1;
              printf("\n%d->%d",j,bv[j]);
            }
            printf("\nFile successfully deleted...");
            strcpy(name[i],"-");
            start[i]=1;
            length[i]=1;
            return;           
          }
     }
}
int main()
{
    int ch=0;
    for (i=0;i<50;i++)
         bv[i]=1;        
    do 
    {
        printf("\n---Select One Of The Option----\n");
        printf("\n1.Show bit Vector :");
        printf("\n2.Create New File :");
        printf("\n3.Delete File :");
        printf("\n4.Exit:\n");
        printf("\nEnter Your Choice :");
        scanf("%d",&ch);
        
        switch (ch)
        {
                case 1: displayBitVector();
                        break;
                case 2: createFile();
                        break;
                case 3: deleteFile();
                        break;
        }
    }
    while(ch!=4);
}
*/