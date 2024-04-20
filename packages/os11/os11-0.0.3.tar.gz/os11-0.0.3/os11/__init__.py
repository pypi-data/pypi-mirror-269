def Slip():
    	print("""  2,6,15,17,25 """)
		
def Slip1():
    	print("""  /*1
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


/*2
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
*/ """)
		
def Slip2():
    	print(""" /*1
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 100
typedef struct dir
{
      char fname[20];
      int start;
      struct dir *next;
}NODE;
NODE *head,*last,*temp,*prev,*dell,*tmp;
int n,bit[MAX],fb=0;

void init()
{
      int i;
      printf("Enter total no. of disk blocks : ");
      scanf("%d",&n);
      for (i=0;i<n;i++)
      {
           bit[i]=rand()%2;
      }
}
void show_bitvector()
{
     int i;
     for (i=0;i<n;i++)
          printf("%d ",bit[i]);
     printf("\n");
}
void show_dir()
{
     NODE *temp;
     int i;
     printf("\nDirectory : ");
     printf("\nFile Name   Allocated Block Number");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("\n %s",temp->fname);
          printf("      %d",temp->start);
     }
     printf("\n\nAllocated Blocks : ");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("%d->",temp->start);
     }
     printf("NULL\n\n");
}
void create()
{
     NODE *p;
     char fname[20];
     int i,j,nob;
     int fb=0;
     printf("Enter file name : ");
     scanf("%s",&fname);
     printf("Enter the no of blocks : ");
     scanf("%d",&nob);
     for (i=0;i<n;i++)
     {
          if (bit[i]==0)
              fb++;
     }
     if (nob>fb)
     {
         printf("Failed to create file %s\n",fname);
         return;
     }
     else
     {
         for (i=0;i<n;i++)
         {
              if (bit[i]==0 && nob!=0)
              {
                  p=(NODE*)malloc(sizeof(NODE));
                  strcpy(p->fname,fname);
                  nob--;
                  bit[i]=1;
                  p->start=i;
                  p->next=NULL;
                  if (head==NULL)
                      head=p;
                  else
                      last->next=p;
                  last=p;
              }
         }
         printf("File %s created successfully \n",fname);
     }
}
void delete()
{
     int i=0;
     NODE *p,*q;
     char fname[20];
     
     temp=head;
     printf("Enter file to be deleted : ");
     scanf("%s",fname);
     
     while (temp!=NULL)
     {
            p=q=head;
            while (p!=NULL)
            {
                   if (strcmp(p->fname,fname)==0)
                       break;
                       
                   q=p;
                   p=p->next;
            }
            
            if (p==NULL)
            {
                return;
            }
            
            if (p==head)
                head=head->next;
            else if (p==last)
            {
                last=q;
                last->next=NULL;
            }
            else
            {
                 q->next=p->next;
            }
            bit[p->start]=0;
            free(p);
            temp=temp->next;
     }
     printf("File %s deleted successfully\n",fname);
}

int main()
{
    int ch;
    init();
    while(1)
    {
        printf("\n-----Menu-----\n");
        printf("\n1.Show bit Vector");
        printf("\n2.Create New File");
        printf("\n3.Show Directory");
        printf("\n4.Delete File");
        printf("\n5.Exit\n");
        printf("\nEnter Your Choice : \n");
        scanf("%d",&ch);
        
        switch (ch)
        {
                case 1: show_bitvector();
                        break;
                case 2: create();
                        break;
                case 3: show_dir();
                        break;
                case 4: delete();
                        break;
                case 5: exit(0);
        }
    }
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
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
    int all_numbers[1000];
    MPI_Gather(local_numbers, elements_per_process, MPI_INT, all_numbers, elements_per_process, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) 
    {
        printf("Generated Numbers:\n");
        for (int i = 0; i < 1000; i++)
        {
          printf("%d ", all_numbers[i]);   
        }
        printf("\n");
    }
    MPI_Finalize();
    return 0;
}
*/

  """)

def Slip3():
    	print(""" /*1
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
*/  """)
		
def Slip4():
    	print("""  /*1
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
*/2

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
} """)
		
def Slip5():
    	print(""" /*1
#include<stdio.h>
#include<string.h>
int n,m,i,j,l,k,flag,safe;
int a[50][50],av[15],max[50][50],finish[10],need[50][50],req[10],tot[20];
char s[50],str[5];

void get_data()
{
     printf("\nEnter number of processes : ");
     scanf("%d",&n);
     printf("\nEnter number of resources : ");
     scanf("%d",&m);
     printf("\nEnter allocation matrix : \n");
     for (i=0;i<n;i++)
     {
        for (j=0;j<m;j++)
        {
            scanf("%d",&a[i][j]);
        }
    }
    printf("\nEnter MAX matrix : \n");
    for (i=0;i<n;i++)
    {
        for (j=0;j<m;j++)
        {
           scanf("%d",&max[i][j]);
        }
    } 
    printf("Enter total instances : ");
    for (i=0;i<m;i++)
    {
      scanf("%d",&tot[i]);
    } 
    for (i=0;i<n;i++)
        finish[i]=0;
}
void put_data()
{
    printf("\n\nAllocation matrix is : \n");
    for (i=0;i<n;i++)
    {
        for (j=0;j<m;j++)
        {
            printf("%d\t",a[i][j]);
        }
        printf("\n");
    }
    printf("\n\nMax Matrix is : \n");
    for (i=0;i<n;i++)
    {
        for (j=0;j<m;j++)
        {
           printf("%d\t",max[i][j]);
        }
        printf("\n");
    }
    printf("\n\nAvailable Array is : \n");
    for (i=0;i<m;i++)
        printf("%d\t",av[i]);
}
void calc_need()
{
    for (i=0;i<n;i++)
    {
        for (j=0;j<m;j++)
        {
           need[i][j] = max[i][j] - a[i][j];
        }
    }
    printf("\n\nNeed Array is : \n");
    for (i=0;i<n;i++)
    {
        for (j=0;j<m;j++)
        {
           printf("%d\t",need[i][j]);
        }
        printf("\n");
    }
}
int check_need(int i)
{
    flag=0;
    for (j=0;j<m;j++)
    {
        if(need[i][j]>av[j])
        {
            flag = 1;
            break;
        }
    }
    return flag;
}
void safe_state()
{
    printf("\n\n");
    strcpy (s,"\0");
    for (i=0;i<n;i++)
    {
        if (check_need(i)==0)
        {
            for (k=0;k<m;k++)
                av[k]=av[k]+a[i][k];
            sprintf(str,"%d",i);
            strcat(s,"P");
            strcat(s,str);
            strcat(s," ");
            puts(s);
        }
        else
            finish[i]=1;
    }
}
void calc_avail()
{
         
    for (i=0;i<m;i++)
    {
        l=0;
        for (j=0;j<n;j++)
        {
            l+=a[j][i];
        }
        av[i]=tot[i]-l;
    }
}
void res_req()
{
    safe = 0;
    printf("Enter the process number : ");
    scanf("%d",&i);
    printf("\nEnter the request : ");
    for (k=0;k<m;k++)
        scanf("%d",&req[k]);
    printf("\nEnter available array : ");
    for (j=0;j<m;j++)
          scanf("%d",&av[j]);
    for (k=0;k<m;k++)
    {
        if (req[k]>need[i][k] || req[k]>av[k])
        {
            safe = 1;
            break;
        }
    } 
    if (safe == 0)
    {
        for (k=0;k<m;k++)
        {
            av[k] = av[k] - req[k];
            a[i][k] = a[i][k] + req[k];
            need[i][k] = need[i][k] - req[k];
        }
        printf("\nNeed array is : \n");
        for (i=0;i<n;i++)
        {
            for (j=0;j<m;j++)
            {
                printf("%d\t",need[i][j]);
            }
            printf("\n");
        }
        put_data();
        printf("The request can be granted.....\n");
    }
    else
        printf("\nThe request can not be granted immediately....\n");
}
void main()
{
    int p,f;
    f=0;
    get_data();
    calc_avail();
    aaa : 
    put_data();
    calc_need();
    safe_state();
     
    for (k=0;k<m;k++)
    {
        if (finish[k]==1)
        {
            if (check_need(k)==0)
            {
                for (p=0;p<m;p++)
                    av[p] = av[p] + a[k][p];
                sprintf(str,"%d",k);
                strcat(s,"P");
                strcat(s,str);
                strcat(s," ");
                finish[k]=1;
            }
            else
                f=1;
        }
    }
    if (f==0)
    {
        printf("System is in safe state.....\n");
        printf("\nSafe Sequence\n");
        puts(s);
    }
    else
        printf("System is not in safe state\n");
    res_req();
    goto aaa;    
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
    int localMax = randomNumbers[0];

    for (int i = 1; i < 1000; i++) 
    {
        if (randomNumbers[i] > localMax) 
        {
            localMax = randomNumbers[i];
        }
    }
    int globalMax;
    MPI_Reduce(&localMax, &globalMax, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0) 
    {
        printf("Maximum number: %d\n", globalMax);
    }
    free(randomNumbers);
    MPI_Finalize();
    return 0;
}
*/
  """)
		
def Slip6():
    	print(""" /*1
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 100
typedef struct dir
{
      char fname[20];
      int start;
      struct dir *next;
}NODE;
NODE *head,*last,*temp,*prev,*dell,*tmp;
int n,bit[MAX],fb=0;
void init()
{
      int i;
      printf("Enter total no. of disk blocks : ");
      scanf("%d",&n);
      for (i=0;i<n;i++)
      {
           bit[i]=rand()%2;
      }
}
void show_bitvector()
{
     int i;
     for (i=0;i<n;i++)
          printf("%d ",bit[i]);
     printf("\n");
}
void show_dir()
{
     NODE *temp;
     int i;
     printf("\nDirectory : ");
     printf("\nFile Name   Allocated Block Number");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("\n %s",temp->fname);
          printf("      %d",temp->start);
     }
     printf("\n\nAllocated Blocks : ");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("%d->",temp->start);
     }
     printf("NULL\n\n");
}
void create()
{
     NODE *p;
     char fname[20];
     int i,j,nob;
     int fb=0;
     printf("Enter file name : ");
     scanf("%s",&fname);
     printf("Enter the no of blocks : ");
     scanf("%d",&nob);
     for (i=0;i<n;i++)
     {
          if (bit[i]==0)
              fb++;
     }
     if (nob>fb)
     {
         printf("Failed to create file %s\n",fname);
         return;
     }
     else
     {
         for (i=0;i<n;i++)
         {
              if (bit[i]==0 && nob!=0)
              {
                  p=(NODE*)malloc(sizeof(NODE));
                  strcpy(p->fname,fname);
                  nob--;
                  bit[i]=1;
                  p->start=i;
                  p->next=NULL;
                  if (head==NULL)
                      head=p;
                  else
                      last->next=p;
                  last=p;
              }
         }
         printf("File %s created successfully \n",fname);
     }
}
void delete()
{
     int i=0;
     NODE *p,*q;
     char fname[20];
     
     temp=head;
     printf("Enter file to be deleted : ");
     scanf("%s",fname);
     
     while (temp!=NULL)
     {
            p=q=head;
            while (p!=NULL)
            {
                   if (strcmp(p->fname,fname)==0)
                       break;
                       
                   q=p;
                   p=p->next;
            }
            
            if (p==NULL)
            {
                return;
            }
            
            if (p==head)
                head=head->next;
            else if (p==last)
            {
                last=q;
                last->next=NULL;
            }
            else
            {
                 q->next=p->next;
            }
            bit[p->start]=0;
            free(p);
            temp=temp->next;
     }
     printf("File %s deleted successfully\n",fname);
}
int main()
{
    int ch;
    init();
    while(1)
    {
        printf("\n-----Menu-----\n");
        printf("\n1.Show bit Vector");
        printf("\n2.Create New File");
        printf("\n3.Show Directory");
        printf("\n4.Delete File");
        printf("\n5.Exit\n");
        printf("\nEnter Your Choice : \n");
        scanf("%d",&ch);
        
        switch (ch)
        {
                case 1: show_bitvector();
                        break;
                case 2: create();
                        break;
                case 3: show_dir();
                        break;
                case 4: delete();
                        break;
                case 5: exit(0);
        }
    }
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
*/  """)
		
def Slip7():
    	print(""" /*1
#include<stdio.h>
int main() 
{   
    int n, m, i, j, k;
    printf("Enter the number of processes: ");
    scanf("%d", &n);
    printf("Enter the number of resources: ");
    scanf("%d", &m);
    int allocation[n][m],max[n][m],need[n][m];
    int available[m],safe_sequence[n],finish[n];

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
            scanf("%d", &max[i][j]);
        }
    }
    for (i = 0; i < n; i++) 
		{
        for (j = 0; j < m; j++) 
				{
            need[i][j] = max[i][j] - allocation[i][j];
        }
    }
    printf("Enter the available resources vector:\n");
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
*/  """)
		
def Slip8():
    	print("""  /*1
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
        printf("\n1.Show bit Vector ");
        printf("\n2.Create New File ");
        printf("\n3.Show Directory ");
        printf("\n4.Exit\n");
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
#include<stdio.h>
#include<stdlib.h>
void main()
{
     int i,n,initial,total=0,min,index,temp,dist,j;
     printf("Enter no. of disk req. : ");
     scanf("%d",&n);
     int req[n];
     printf("Enter disk request queue :\n");
     for (i=0;i<n;i++)
          scanf("%d",&req[i]);
     printf("Enter initial head position : ");
     scanf("%d",&initial);
     for (i=0;i<n;i++)
     {
          min= abs(req[i]-initial);
          index = i;
          for (j=i+1;j<n;j++)
          {
              dist = abs(req[j]-initial);
              if (dist<=min)
              {
                 min=dist;
                 index=j;
              }
          }
          total+=min;
          temp=req[i];
          req[i]=req[index];
          req[index]=temp;
          initial=req[i];
     }
     printf("Total head movements : %d\n",total);          
}
*/ """)
		
def Slip9():
    	print("""  /*1
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
*/ """)
		
def Slip10():
    	print(""" /*1
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
*/  """)
		
def Slip11():
    	print(""" /*1
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



  """)
		
def Slip12():
    	print(""" /*1
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
*/  """)
		
def Slip13():
    	print("""  /*1
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
*/ """)
		
def Slip14():
    	print(""" /*1
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
        printf("\n3.Show Directory :");
        printf("\n4.Delete File :");
        printf("\n5.Exit:\n");
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
                case 4: deleteFile();
                        break;
        }
    }
    while(ch!=5);
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
void main()
{
     int i,n,initial,total=0,min,index,temp,dist,j;
     printf("Enter no. of disk req. : ");
     scanf("%d",&n);
     int req[n];
     printf("Enter disk request queue :\n");
     for (i=0;i<n;i++)
          scanf("%d",&req[i]);
     printf("Enter initial head position : ");
     scanf("%d",&initial);
     for (i=0;i<n;i++)
     {
          min= abs(req[i]-initial);
          index = i;
          for (j=i+1;j<n;j++)
          {
              dist = abs(req[j]-initial);
              if (dist<=min)
              {
                 min=dist;
                 index=j;
              }
          }
          total+=min;
          temp=req[i];
          req[i]=req[index];
          req[index]=temp;
          initial=req[i];
     }
     printf("Total head movements : %d\n",total);          
}
*/  """)
		
def Slip15():
    	print(""" /*1
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 100
typedef struct dir
{
      char fname[20];
      int start;
      struct dir *next;
}NODE;
NODE *head,*last,*temp,*prev,*dell,*tmp;
int n,bit[MAX],fb=0;

void init()
{
      int i;
      printf("Enter total no. of disk blocks : ");
      scanf("%d",&n);
      for (i=0;i<n;i++)
      {
           bit[i]=rand()%2;
      }
}
void show_bitvector()
{
     int i;
     for (i=0;i<n;i++)
          printf("%d ",bit[i]);
     printf("\n");
}
void show_dir()
{
     NODE *temp;
     int i;
     printf("\nDirectory : ");
     printf("\nFile Name   Allocated Block Number");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("\n %s",temp->fname);
          printf("      %d",temp->start);
     }
     printf("\n\nAllocated Blocks : ");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("%d->",temp->start);
     }
     printf("NULL\n\n");
}
void create()
{
     NODE *p;
     char fname[20];
     int i,j,nob;
     int fb=0;
     printf("Enter file name : ");
     scanf("%s",&fname);
     printf("Enter the no of blocks : ");
     scanf("%d",&nob);
     for (i=0;i<n;i++)
     {
          if (bit[i]==0)
              fb++;
     }
     if (nob>fb)
     {
         printf("Failed to create file %s\n",fname);
         return;
     }
     else
     {
         for (i=0;i<n;i++)
         {
              if (bit[i]==0 && nob!=0)
              {
                  p=(NODE*)malloc(sizeof(NODE));
                  strcpy(p->fname,fname);
                  nob--;
                  bit[i]=1;
                  p->start=i;
                  p->next=NULL;
                  if (head==NULL)
                      head=p;
                  else
                      last->next=p;
                  last=p;
              }
         }
         printf("File %s created successfully \n",fname);
     }
}
void delete()
{
     int i=0;
     NODE *p,*q;
     char fname[20];
     
     temp=head;
     printf("Enter file to be deleted : ");
     scanf("%s",fname);
     
     while (temp!=NULL)
     {
            p=q=head;
            while (p!=NULL)
            {
                   if (strcmp(p->fname,fname)==0)
                       break;
                       
                   q=p;
                   p=p->next;
            }
            
            if (p==NULL)
            {
                return;
            }
            
            if (p==head)
                head=head->next;
            else if (p==last)
            {
                last=q;
                last->next=NULL;
            }
            else
            {
                 q->next=p->next;
            }
            bit[p->start]=0;
            free(p);
            temp=temp->next;
     }
     printf("File %s deleted successfully\n",fname);
}

int main()
{
    int ch;
    init();
    while(1)
    {
        printf("\n-----Menu-----\n");
        printf("\n1.Show bit Vector");
        printf("\n2.Create New File");
        printf("\n3.Show Directory");
        printf("\n4.Delete File");
        printf("\n5.Exit\n");
        printf("\nEnter Your Choice : \n");
        scanf("%d",&ch);
        
        switch (ch)
        {
                case 1: show_bitvector();
                        break;
                case 2: create();
                        break;
                case 3: show_dir();
                        break;
                case 4: delete();
                        break;
                case 5: exit(0);
        }
    }
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
*/  """)
		
def Slip16():
    	print(""" /*1
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
  """)

		
def Slip18():
    	print(""" /*1
#include <stdio.h>
#include<stdlib.h>
int files[10], indexBlock[50], indBlock, n,cnt=0;
char  fnm[20],f[20];
int main()
{
    FILE *fp;
    static  int sb,len;
    int t;
    int op=1;

    printf("Enter Total Block : ");
    scanf("%d",&t);
    files[t];

    for(int i=0; i<10; i++)
        files[i]=1;

    printf("Bit Vector Before Allocation \n ");
    for(int i=0; i<t; i++)
        printf("%d",files[i]);

    printf("\n");
    while(op>=1 && op<=5)
    {

      y:  printf("\n 1.Create File");
        printf("\n 2.Show bit Vector ");
        printf("\n 3.Delete File  ");
        printf("\n 4.Display Directory ");
        printf("\n 5.Exit");

        printf("\n Enter option :  ");
        scanf("%d",&op);
        switch(op)
        {
        case 1:
            printf("\nEnter File name : ");
            scanf("%s",fnm);
            fp = fopen(fnm, "w");

            if (fp == NULL) 
            {
                printf("\nError opening the file.\n");
                return 1;
            }
            else
                printf("\n * File is created * \n ");

           x: printf("Enter the index block: ");
            scanf("%d", &indBlock);
            if (files[indBlock] != 0)
            {
                files[indBlock]=0;
                printf("\nEnter the number of blocks  needed for the index %d on the disk: ", indBlock);
                scanf("%d", &n);
            }
            else 
            {
                printf("%d is already allocated\n", indBlock);
                goto x;
            }

        int flag = 0;
        cnt=0;

       z: printf("\nEnter block occupied by given %s File : \n ",fnm);
        for (int i=0; i<n; i++) 
        {
            scanf("%d", &indexBlock[i]);
            cnt++;
            if (files[indexBlock[i]] == 1)
                flag++;
        }
        if (flag == n) 
        {
            for (int j=0; j<n; j++) 
            {
                files[indexBlock[j]] = 0;
            }
            printf("\n**Allocated***\n");
            printf("\nFNm\tIB\tIndex\tAlloctated\n");
            for (int k=0; k<n; k++) {
                printf("%s\t%d ----> %d\t%d\n", fnm,indBlock, indexBlock[k], files[indexBlock[k]]);
            }
            goto y;
        }
        else 
        {
            printf(" block is already allocated\n");
            printf("Enter another blocks\n");
            goto z;
        }   
    break;
case 2 :
    printf("\n Bit Vector After  Allocation \n ");
    for(int i=0; i<t; i++)
        printf("%d",files[i]);
    printf("\n");
    break;
case 3:
    printf("\nEnter File name to delete : ");
    scanf("%s",&f);
    if (remove(f) == 0)
        printf("\nDeleted successfully\n");
    else
        printf("\nUnable to delete the file\n");
    break;
case 4 :
    printf("\n File Details Are : \n ");
    printf("\nF_NM\tIB\tLen\n");
    printf("%s\t%d\t%d",fnm,indBlock,cnt);
    printf("\n");
    break;
case 5 :
    exit(0);
}
if(op!=4 )
{
    printf("\nF_NM\tIB\tLen\n");
    printf("%s\t%d\t%d",fnm,indBlock,cnt);
    printf("\n");
}
}
fclose(fp);
return 0;
}
*/


/*2
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
*/  """)
		
def Slip19():
    	print(""" /*1
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
*/  """)
		
def Slip20():
    	print(""" /*1
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
    int localMax = randomNumbers[0];

    for (int i = 1; i < 1000; i++) 
    {
        if (randomNumbers[i] > localMax) 
        {
            localMax = randomNumbers[i];
        }
    }
    int globalMax;
    MPI_Reduce(&localMax, &globalMax, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0) 
    {
        printf("Maximum number: %d\n", globalMax);
    }
    free(randomNumbers);
    MPI_Finalize();
    return 0;
}
*/
  """)
		
def Slip21():
    	print(""" /*1
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
*/  """)
		
def Slip22():
    	print("""  /*1
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
*/ """)
		
def Slip23():
    	print(""" /*1
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
*/  """)
		
def Slip24():
    	print("""  /*1
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
 """)
		
def Slip25():
    	print(""" /*1
#include<stdio.h>
#include<stdlib.h>
int main()
{
    int initial_head_pos, direction, num_requests,temp,total_seek=0,current_head_pos;
    float avg_seek_time;
    
    printf("Enter initial head position : ");
    scanf("%d",&initial_head_pos);
    
    printf("Enter the direction (0 for left 1 for right) : ");
    scanf("%d",&direction);
    
    printf("Enter the number of disk requests : ");
    scanf("%d",&num_requests);
    
    int request_queue[num_requests];
    
    printf("Enter the disk queue : ");
    for (int i=0;i<num_requests;i++)
    {
         scanf("%d",&request_queue[i]);
    }    
    for (int i=0;i<num_requests-1;i++)
    {
         for (int j=0;j<num_requests-1;j++)
         {
              if (request_queue[j]>request_queue[j+1])
              {
                  temp = request_queue[j];
                  request_queue[j]=request_queue[j+1];
                  request_queue[j+1]=temp;
              }
         }
    }
    int i;
    for (i=0;i<num_requests;i++)
    {
         if (request_queue[i]>=initial_head_pos)
             break;
    }
    current_head_pos=initial_head_pos;
    if (direction==1)
    {
        for (int j=i;j<num_requests;j++)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos = request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        } 
        for (int j=i-1;j>=0;j--)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos=request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
    }
    else
    {
        for (int j=i-1;j>=0;j--)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos=request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
        for (int j=i;j<num_requests;j++)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos = request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
    }
    printf("Total seek movement : %d\n",total_seek);    
    return 0;
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 100
typedef struct dir
{
      char fname[20];
      int start;
      struct dir *next;
}NODE;
NODE *head,*last,*temp,*prev,*dell,*tmp;
int n,bit[MAX],fb=0;
void init()
{
      int i;
      printf("Enter total no. of disk blocks : ");
      scanf("%d",&n);
      for (i=0;i<n;i++)
      {
           bit[i]=rand()%2;
      }
}
void show_bitvector()
{
     int i;
     for (i=0;i<n;i++)
          printf("%d ",bit[i]);
     printf("\n");
}
void show_dir()
{
     NODE *temp;
     int i;
     printf("\nDirectory : ");
     printf("\nFile Name Allocated Block Number");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("\n %s",temp->fname);
          printf("      %d",temp->start);
     }
     printf("\n\nAllocated Blocks : ");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("%d->",temp->start);
     }
     printf("NULL\n\n");
}
void create()
{
     NODE *p;
     char fname[20];
     int i,j,nob;
     int fb=0;
     printf("Enter file name : ");
     scanf("%s",&fname);
     printf("Enter the no of blocks : ");
     scanf("%d",&nob);
     for (i=0;i<n;i++)
     {
          if (bit[i]==0)
              fb++;
     }
     if (nob>fb)
     {
         printf("Failed to create file %s\n",fname);
         return;
     }
     else
     {
         for (i=0;i<n;i++)
         {
              if (bit[i]==0 && nob!=0)
              {
                  p=(NODE*)malloc(sizeof(NODE));
                  strcpy(p->fname,fname);
                  nob--;
                  bit[i]=1;
                  p->start=i;
                  p->next=NULL;
                  if (head==NULL)
                      head=p;
                  else
                      last->next=p;
                  last=p;
              }
         }
         printf("File %s created successfully \n",fname);
     }
}
int main()
{
    int ch;
    init();
    while(1)
    {
        printf("\n-----Menu-----\n");
        printf("\n1.Show bit Vector");
        printf("\n2.Create New File");
        printf("\n3.Show Directory");
        printf("\n4.Exit\n");
        printf("\nEnter Your Choice : \n");
        scanf("%d",&ch);  
        switch (ch)
        {
                case 1: show_bitvector();
                        break;
                case 2: create();
                        break;
                case 3: show_dir();
                        break;
                case 4: exit(0);
        }
    }
}
*/  """)
		
def Slip26():
    	print(""" /*1
#include<stdio.h>
#include<stdlib.h>
int main()
{
    int initial_head_pos, direction, num_requests,temp,total_seek=0,current_head_pos;
    float avg_seek_time;
    
    printf("Enter initial head position : ");
    scanf("%d",&initial_head_pos);
    
    printf("Enter the direction (0 for left 1 for right) : ");
    scanf("%d",&direction);
    
    printf("Enter the number of disk requests : ");
    scanf("%d",&num_requests);
    
    int request_queue[num_requests];
    
    printf("Enter the disk queue : ");
    for (int i=0;i<num_requests;i++)
    {
         scanf("%d",&request_queue[i]);
    }    
    for (int i=0;i<num_requests-1;i++)
    {
         for (int j=0;j<num_requests-1;j++)
         {
              if (request_queue[j]>request_queue[j+1])
              {
                  temp = request_queue[j];
                  request_queue[j]=request_queue[j+1];
                  request_queue[j+1]=temp;
              }
         }
    }
    int i;
    for (i=0;i<num_requests;i++)
    {
         if (request_queue[i]>=initial_head_pos)
             break;
    }
    current_head_pos=initial_head_pos;
    if (direction==1)
    {
        for (int j=i;j<num_requests;j++)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos = request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        } 
        for (int j=i-1;j>=0;j--)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos=request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
    }
    else
    {
        for (int j=i-1;j>=0;j--)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos=request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
        for (int j=i;j<num_requests;j++)
        {
             total_seek+=abs(request_queue[j]-current_head_pos);
             current_head_pos = request_queue[j];
             printf("Head Moving towards %d\n",current_head_pos);
        }
    }
    printf("Total seek movement : %d\n",total_seek);    
    return 0;
}
*/


/*2
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 100
typedef struct dir
{
      char fname[20];
      int start;
      struct dir *next;
}NODE;
NODE *head,*last,*temp,*prev,*dell,*tmp;
int n,bit[MAX],fb=0;
void init()
{
      int i;
      printf("Enter total no. of disk blocks : ");
      scanf("%d",&n);
      for (i=0;i<n;i++)
      {
           bit[i]=rand()%2;
      }
}
void show_bitvector()
{
     int i;
     for (i=0;i<n;i++)
          printf("%d ",bit[i]);
     printf("\n");
}
void show_dir()
{
     NODE *temp;
     int i;
     printf("\nDirectory : ");
     printf("\nFile Name Allocated Block Number");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("\n %s",temp->fname);
          printf("      %d",temp->start);
     }
     printf("\n\nAllocated Blocks : ");
     for (temp=head;temp!=NULL;temp=temp->next)
     {
          printf("%d->",temp->start);
     }
     printf("NULL\n\n");
}
void create()
{
     NODE *p;
     char fname[20];
     int i,j,nob;
     int fb=0;
     printf("Enter file name : ");
     scanf("%s",&fname);
     printf("Enter the no of blocks : ");
     scanf("%d",&nob);
     for (i=0;i<n;i++)
     {
          if (bit[i]==0)
              fb++;
     }
     if (nob>fb)
     {
         printf("Failed to create file %s\n",fname);
         return;
     }
     else
     {
         for (i=0;i<n;i++)
         {
              if (bit[i]==0 && nob!=0)
              {
                  p=(NODE*)malloc(sizeof(NODE));
                  strcpy(p->fname,fname);
                  nob--;
                  bit[i]=1;
                  p->start=i;
                  p->next=NULL;
                  if (head==NULL)
                      head=p;
                  else
                      last->next=p;
                  last=p;
              }
         }
         printf("File %s created successfully \n",fname);
     }
}
int main()
{
    int ch;
    init();
    while(1)
    {
        printf("\n-----Menu-----\n");
        printf("\n1.Show bit Vector");
        printf("\n2.Create New File");
        printf("\n3.Show Directory");
        printf("\n4.Exit\n");
        printf("\nEnter Your Choice : \n");
        scanf("%d",&ch);  
        switch (ch)
        {
                case 1: show_bitvector();
                        break;
                case 2: create();
                        break;
                case 3: show_dir();
                        break;
                case 4: exit(0);
        }
    }
}
*/  """)
		
def Slip27():
    	print(""" /*1
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
*/  """)
		
def Slip28():
    	print("""  
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
*/ """)
		
def Slip29():
    	print("""  /*1
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
*/ """)
		
def Slip30():
    	print(""" /*1
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


/*2
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
*/  """)
