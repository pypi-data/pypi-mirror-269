/*1
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
void showDirectory()
{
      printf("Directory contents\n");
      printf("%s%s%s\n","File Name","Start Block","Length");
      int i;
      for (i=0;i<num;i++)
      {
           if (strcmp(name[i],"-")!=0)
           {
               printf("  %s    %d   %d\n",name[i],start[i],length[i]);
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
        printf("\n3.Show Directory :");
        printf("\n4.Exit:\n");
        printf("\nEnter Your Choice :");
        scanf("%d",&ch);
        
        switch (ch)
        {
                case 1: displayBitVector();
                        break;
                case 2: createFile();
                        break;
                case 3: showDirectory();
                        break;
        }
    }
    while(ch!=4);
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
