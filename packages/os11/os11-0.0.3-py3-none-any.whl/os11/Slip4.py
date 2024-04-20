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

#include<stdio.h>
#include<stdlib.h>
int main()
{
	int q[100],j,n,i,seek=0,max,head,move;
	printf("\n Enter the number of request: ");
	scanf("%d",&n);
	printf("\n Enter the request sequence: ");
	for(i=0;i<n;i++)
		scanf("%d",&q[i]);
	printf("\n Enter initial head position: ");
	scanf("%d",&head);
	printf("\n Enter total disk size: ");
	scanf("%d",&max);
	printf("\n Enter the head movement direction for high 1 and for low 0: ");
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
	
	printf("\n Sequence of head movement: ");
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
		head=max-1;
		printf("%d\t",head);
		for(i=index-1;i>=0;i--)
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
		head=0;
		printf("%d\t",head);
		for(i=index;i<n;i++)
		{
			seek+=abs(q[i]-head);
			head=q[i];
			printf("%d\t",q[i]);
		}
	}
	printf("\n\n Total head movement are %d",seek);
	return 0;
}