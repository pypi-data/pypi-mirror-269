/*
#include<stdio.h>
void main()
{
     int n,i,p[10],r,a[10][10],j,max[10][10],av[10],need[10][10];
     char res;
     
     printf("\nEnter the No of Processes : ");
     scanf("%d",&n);
     
     printf("\nEnter the No of Resources : ");
     scanf("%d",&r);
     
     printf("\nEnter the Allocation Matrix :");
     for (i=0;i<n;i++)
         for (j=0;j<r;j++)
             scanf("%d",&a[i][j]);
     
     printf("\nEnter Max Matrix :\n");
     for (i=0;i<n;i++)
         for (j=0;j<r;j++)
             scanf("%d",&max[i][j]);
     
     printf("\nEnter Available : ");
     for (i=0;i<r;i++)
         scanf("%d",&av[i]);
     
     printf("\nAllocation Matrix : \n");
     for (i=0;i<n;i++)
     {
         printf("\n");
         for (j=0;j<r;j++)
             printf("%d\t",a[i][j]);
     } 
     printf("\nMax Allocation Matrix :\n ");
     for ( i=0;i<n;i++)
     {
        printf("\np%d\t",i);
        for(j=0;j<r;j++)
            printf("%d\t",max[i][j]);
     }
     printf("\n Need Matrix : ");
     for (i=0;i<n;i++)
     {
         printf("\n%d\t",i);
         for (j=0;j<r;j++)
         {
             need[i][j]=max[i][j]-a[i][j];
             printf("%d\t",need[i][j]);
         }
     }
     printf("\n Available Array Is: ");
     for (i=0;i<n;i++)
         if (i==0)
            for (j=0;j<r;j++)
                printf("%d  ",av[j]);
}
*/


/*
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