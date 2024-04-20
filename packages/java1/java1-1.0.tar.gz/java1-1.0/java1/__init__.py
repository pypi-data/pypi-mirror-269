def slip1():
    print("""
1.
#define true 1
#define false 0
#include <stdio.h>
#include <ctype.h>
int avail[4], work[10];
int max[5][4], alloc[5][4];
int need[5][4], finish[10], req[10];
int m = 3, n = 5;
int i, j;
void main()
{
printf("\n Total number of resource type:%d", m);
printf("\n Total number of processes:%d", n);
int choice = 0;
while (choice != 8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Exit\nEnter your choice:");
scanf("%d", &choice);
switch (choice)
{
case 1:
printf("\nEnter available:");
for (j = 0; j < m; j++)
{
scanf("%d", &avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
scanf("%d", &max[i][j]);
}
printf("\nEnter allocation by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
scanf("%d", &alloc[i][j]);
}
break;
case 2:
printf("\nMaximum demand by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
printf("%d\t", max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
printf("%d\t", alloc[i][j]);
printf("\n");
}
break;
case 3:
printf("\nNeed Matrix:");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
{
need[i][j] = max[i][j] - alloc[i][j];
printf("%4d\t", need[i][j]);
}
printf("\n");
}
break;
case 4:
printf("\nAvailable:");
for (j = 0; j < m; j++)
printf("%d\t", avail[j]);
break;
case 5:
printf("\nRequest of process number?");
scanf("%d", &i);
printf("\nEnter request:");
for (j = 0; j < m; j++)
scanf("%d", &req[i]);
break;
case 6:
choice = 6;
break;
default:
printf("Invalid Choice");
}
}
}

2.          
#include<stdio.h>
#include<stdlib.h>
int main()
{
int n, rq[20], initial, totalhm, i;
printf("\nEnter no of request:");
scanf("%d",&n);
printf("\nEnter the request sequence:");
for(i=0;i<n;i++)
scanf("%d",&rq[i]);
printf("\nenter head position:");
scanf("%d",&initial);
for(i=0;i<n;i++)
{
totalhm=totalhm+abs(rq[i]-initial);
initial=rq[i];
}
printf("\nTotal head moment is %d",totalhm);
return 0;
}
              """)
def slip3():
    print("""
1.
#define true 1
#define false 0
#include<stdio.h>
#include<ctype.h>
int avail[4],work[10];
int max[5][4],alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3,n=5;
int i,j;
void get_alloc_state();
void print_safeseq();
void get_alloc_request();
void main()
{
get_alloc_state();
}
void get_alloc_state()
{
printf("\n Total number of resource type:%d",m);
printf("\n Total number of processes:%d",n);
int choice=0;
while(choice!=8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Safety algorithm\n7.Resource request agorithm\n8.Exit\nEnter your choice:");
scanf("%d",&choice);
switch(choice)
{
case 1:printf("\nEnter available:");
for(j=0;j<m;j++)
{
scanf("%d",&avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&max[i][j]);
}
printf("\nEnter allocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&alloc[i][j]);
}
break;
case 2: printf("\nMaximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",alloc[i][j]);
printf("\n");
}
break;
case 3:printf("\nNeed Matrix:");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
{
need[i][j]=max[i][j]-alloc[i][j];
printf("%4d\t",need[i][j]);
}
printf("\n");
}
break;
case 4:printf("\nAvailable:");
for(j=0;j<m;j++)
printf("%d\t",avail[j]);
break;
case 5:printf("\nRequest of process number?");
scanf("%d",&i);
printf("\nEnter request:");
for(j=0;j<m;j++)
scanf("%d",&req[i]);
break;
case 6:if(safe_state())
{
printf("\nGiven system is in safe state....");
print_safeseq();
}
break;
case 7:if(safe_state())
{
printf("\nGiven system is in safe state....");
ssi=ssi/2;
print_safeseq();
}
else
{
printf("\nGiven system is not in safe state....");
get_alloc_request();
ssi=-1;
if(safe_state())
{
printf("\nSystem will be in safe state after request....");
print_safeseq();
}
else
{
printf("\nSystem will be not in safe state after request....");
printf("\nAllocation state is undone ...");
printf("\nProcess requesting should wait....");
}
}
break;
case 8:choice=8;
break;
default:printf("Invalid Choice");
}
}
}
safe_state()
{
int found;
for(j=0;j<m;j++)
work[j]=avail[j];
for(i=0;i<n;i++)
finish[i]=false;
printf("\nCheck of safe state...");
do
{
found=false;
for(i=0;i<n;i++)
{
if(finish[i]==false && need_lte_work(i))
{
printf("\nSelected process %d",i);
finish[i]=true;
for(j=0;j<m;j++)
work[j]=work[j]+alloc[i][j];
safeseq[++ssi]=i;
found=true;
}
}
if(found==false)
{
for(i=0;i<n;i++)
if(finish[i]==false)
return(false);
return(true);
}
}while(1);
}
need_lte_work(int i)
{
for(j=0;j<m;j++)
{
if(need[i][j]>work[j])
{
return false;
}
return true;
}
}
void print_safeseq()
{
printf("\n\nSafe sequence:");
for(i=0;i<=ssi;i++)
printf("%4d",safeseq[i]);
}
void get_alloc_request()
{
if(!req_lte_need(i))
{
printf("\n Process requested more than its max claim...");
}
if(!req_lte_avail(i))
{
printf("\n Resources are not available.Pocess %d should wait..",i);
}
for(j=0;j<m;j++)
{
alloc[i][j]+=req[j];
need[i][j]-=req[j];
avail[j]-=req[j];
}
}
req_lte_need(int i)
{
for(j=0;j<m;j++)
{
if (req[j] >need[i][j])
return 0;
}
return 1;
}
req_lte_avail()
{
for(j=0; j<m; j++)
{
if(req[j]>avail[j])
return 0;
}
return 1;
}
          
2.
          
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float local_sum=0;
int i;
for(i=0; i<num_elements_per_proc; i++)
{
local_sum += rand_nums[i];
}
printf("\nLocal sum for process %d-%f. avg=%f\n", world_rank, local_sum, local_sum/num_elements_per_proc);
float global_sum;
MPI_Reduce(&local_sum, &global_sum, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nTotal sum=%f.avg = %f\n", global_sum, global_sum/(world_size=num_elements_per_proc));
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();          
    """)
def slip4():
    print("""
1.
#define true 1
#define false 0
#include <stdio.h>
#include <ctype.h>
int avail[4], work[10];
int max[5][4], alloc[5][4];
int need[5][4], finish[10], req[10];
int m = 3, n = 5;
int i, j;
void main()
{
printf("\n Total number of resource type:%d", m);
printf("\n Total number of processes:%d", n);
int choice = 0;
while (choice != 8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Exit\nEnter your choice:");
scanf("%d", &choice);
switch (choice)
{
case 1:
printf("\nEnter available:");
for (j = 0; j < m; j++)
{
scanf("%d", &avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
scanf("%d", &max[i][j]);
}
printf("\nEnter allocation by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
scanf("%d", &alloc[i][j]);
}
break;
case 2:
printf("\nMaximum demand by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
printf("%d\t", max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
printf("%d\t", alloc[i][j]);
printf("\n");
}
break;
case 3:
printf("\nNeed Matrix:");
for (i = 0; i < n; i++)
{
printf("Process:%d", i);
for (j = 0; j < m; j++)
{
need[i][j] = max[i][j] - alloc[i][j];
printf("%4d\t", need[i][j]);
}
printf("\n");
}
break;
case 4:
printf("\nAvailable:");
for (j = 0; j < m; j++)
printf("%d\t", avail[j]);
break;
case 5:
printf("\nRequest of process number?");
scanf("%d", &i);
printf("\nEnter request:");
for (j = 0; j < m; j++)
scanf("%d", &req[i]);
break;
case 6:
choice = 6;
break;
default:
printf("Invalid Choice");
}
}
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, count=0, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		initial = size-1;
		
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(RQ[i+1]-0);
		initial = 0;
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
                    
    """)
def slip5():
    print("""
1.
#define true 1
#define false 0
#include<stdio.h>
#include<ctype.h>
int avail[4],work[10];
int max[5][4],alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3,n=5;
int i,j;
void get_alloc_state();
void print_safeseq();
void get_alloc_request();
void main()
{
get_alloc_state();
}
void get_alloc_state()
{
printf("\n Total number of resource type:%d",m);
printf("\n Total number of processes:%d",n);
int choice=0;
while(choice!=8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Safety algorithm\n7.Resource request agorithm\n8.Exit\nEnter your choice:");
scanf("%d",&choice);
switch(choice)
{
case 1:printf("\nEnter available:");
for(j=0;j<m;j++)
{
scanf("%d",&avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&max[i][j]);
}
printf("\nEnter allocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&alloc[i][j]);
}
break;
case 2: printf("\nMaximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",alloc[i][j]);
printf("\n");
}
break;
case 3:printf("\nNeed Matrix:");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
{
need[i][j]=max[i][j]-alloc[i][j];
printf("%4d\t",need[i][j]);
}
printf("\n");
}
break;
case 4:printf("\nAvailable:");
for(j=0;j<m;j++)
printf("%d\t",avail[j]);
break;
case 5:printf("\nRequest of process number?");
scanf("%d",&i);
printf("\nEnter request:");
for(j=0;j<m;j++)
scanf("%d",&req[i]);
break;
case 6:if(safe_state())
{
printf("\nGiven system is in safe state....");
print_safeseq();
}
break;
case 7:if(safe_state())
{
printf("\nGiven system is in safe state....");
ssi=ssi/2;
print_safeseq();
}
else
{
printf("\nGiven system is not in safe state....");
get_alloc_request();
ssi=-1;
if(safe_state())
{
printf("\nSystem will be in safe state after request....");
print_safeseq();
}
else
{
printf("\nSystem will be not in safe state after request....");
printf("\nAllocation state is undone ...");
printf("\nProcess requesting should wait....");
}
}
break;
case 8:choice=8;
break;
default:printf("Invalid Choice");
}
}
}
safe_state()
{
int found;
for(j=0;j<m;j++)
work[j]=avail[j];
for(i=0;i<n;i++)
finish[i]=false;
printf("\nCheck of safe state...");
do
{
found=false;
for(i=0;i<n;i++)
{
if(finish[i]==false && need_lte_work(i))
{
printf("\nSelected process %d",i);
finish[i]=true;
for(j=0;j<m;j++)
work[j]=work[j]+alloc[i][j];
safeseq[++ssi]=i;
found=true;
}
}
if(found==false)
{
for(i=0;i<n;i++)
if(finish[i]==false)
return(false);
return(true);
}
}while(1);
}
need_lte_work(int i)
{
for(j=0;j<m;j++)
{
if(need[i][j]>work[j])
{
return false;
}
return true;
}
}
void print_safeseq()
{
printf("\n\nSafe sequence:");
for(i=0;i<=ssi;i++)
printf("%4d",safeseq[i]);
}
void get_alloc_request()
{
if(!req_lte_need(i))
{
printf("\n Process requested more than its max claim...");
}
if(!req_lte_avail(i))
{
printf("\n Resources are not available.Pocess %d should wait..",i);
}
for(j=0;j<m;j++)
{
alloc[i][j]+=req[j];
need[i][j]-=req[j];
avail[j]-=req[j];
}
}
req_lte_need(int i)
{
for(j=0;j<m;j++)
{
if (req[j] >need[i][j])
return 0;
}
return 1;
}
req_lte_avail()
{
for(j=0; j<m; j++)
{
if(req[j]>avail[j])
return 0;
}
return 1;
}

2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}          
    """)
def slip7():
    print("""
1.
#define true 1
#define false 0
#include<stdio.h>
#include<ctype.h>
int avail[4],work[10];
int max[5][4],alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3,n=5;
int i,j;
void get_alloc_state();
void print_safeseq();
void get_alloc_request();
void main()
{
get_alloc_state();
}
void get_alloc_state()
{
printf("\n Total number of resource type:%d",m);
printf("\n Total number of processes:%d",n);
int choice=0;
while(choice!=8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Safety algorithm\n7.Resource request agorithm\n8.Exit\nEnter your choice:");
scanf("%d",&choice);
switch(choice)
{
case 1:printf("\nEnter available:");
for(j=0;j<m;j++)
{
scanf("%d",&avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&max[i][j]);
}
printf("\nEnter allocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&alloc[i][j]);
}
break;
case 2: printf("\nMaximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",alloc[i][j]);
printf("\n");
}
break;
case 3:printf("\nNeed Matrix:");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
{
need[i][j]=max[i][j]-alloc[i][j];
printf("%4d\t",need[i][j]);
}
printf("\n");
}
break;
case 4:printf("\nAvailable:");
for(j=0;j<m;j++)
printf("%d\t",avail[j]);
break;
case 5:printf("\nRequest of process number?");
scanf("%d",&i);
printf("\nEnter request:");
for(j=0;j<m;j++)
scanf("%d",&req[i]);
break;
case 6:if(safe_state())
{
printf("\nGiven system is in safe state....");
print_safeseq();
}
break;
case 7:if(safe_state())
{
printf("\nGiven system is in safe state....");
ssi=ssi/2;
print_safeseq();
}
else
{
printf("\nGiven system is not in safe state....");
get_alloc_request();
ssi=-1;
if(safe_state())
{
printf("\nSystem will be in safe state after request....");
print_safeseq();
}
else
{
printf("\nSystem will be not in safe state after request....");
printf("\nAllocation state is undone ...");
printf("\nProcess requesting should wait....");
}
}
break;
case 8:choice=8;
break;
default:printf("Invalid Choice");
}
}
}
safe_state()
{
int found;
for(j=0;j<m;j++)
work[j]=avail[j];
for(i=0;i<n;i++)
finish[i]=false;
printf("\nCheck of safe state...");
do
{
found=false;
for(i=0;i<n;i++)
{
if(finish[i]==false && need_lte_work(i))
{
printf("\nSelected process %d",i);
finish[i]=true;
for(j=0;j<m;j++)
work[j]=work[j]+alloc[i][j];
safeseq[++ssi]=i;
found=true;
}
}
if(found==false)
{
for(i=0;i<n;i++)
if(finish[i]==false)
return(false);
return(true);
}
}while(1);
}
need_lte_work(int i)
{
for(j=0;j<m;j++)
{
if(need[i][j]>work[j])
{
return false;
}
return true;
}
}
void print_safeseq()
{
printf("\n\nSafe sequence:");
for(i=0;i<=ssi;i++)
printf("%4d",safeseq[i]);
}
void get_alloc_request()
{
if(!req_lte_need(i))
{
printf("\n Process requested more than its max claim...");
}
if(!req_lte_avail(i))
{
printf("\n Resources are not available.Pocess %d should wait..",i);
}
for(j=0;j<m;j++)
{
alloc[i][j]+=req[j];
need[i][j]-=req[j];
avail[j]-=req[j];
}
}
req_lte_need(int i)
{
for(j=0;j<m;j++)
{
if (req[j] >need[i][j])
return 0;
}
return 1;
}
req_lte_avail()
{
for(j=0; j<m; j++)
{
if(req[j]>avail[j])
return 0;
}
return 1;
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, count=0, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		initial = size-1;
		
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(RQ[i+1]-0);
		initial = 0;
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
    """)
def slip8():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 200

typedef struct dir
{
	char fname[20];
	int start,length;
	struct dir *next;
}NODE;

NODE *first,*last;
int bit[MAX],n;
void init()
{
	int i;
	printf("Enter total no of disk blocks");
	scanf("%d",&n);
	
	for(i=0;i<10;i++)
	{
		int k=rand()%2;
		bit[k]=1;
	}
}

void show_bitvector()
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d",bit[i]);
	}
	printf("\n");
}

void show_dir()
{
	NODE *p;
	printf("File\tstart\tlength\n");
	p=first;
	while(p!=NULL)
	{
		printf("%s\t%d\t%d\n",p->fname,p->start,p->length);
		p=p->next;
	}
}

void create()
{
	NODE *p;
	char fname[20];
	int nob,i=0,j=0,start;
	printf("Enter the file name:");
	scanf("%s",fname);
	
	printf("Enter no of blocks");
	scanf("%d",&nob);

	while(1)
	{
		while(i<n)
		{	
			if(bit[i]==0)
			break;
			i++;
		}
		if(i<n)
		{
		start=i;
		j=1;
		
		while(j<nob&&i<n&&bit[i]==0)
		{
			i++;
			j++;
		}
		if(j==nob)
		{
			p=(NODE*)malloc(sizeof(NODE));
			strcpy(p->fname,fname);
			p->start=start;
			p->length=nob;
			p->next=NULL;
				if(first==NULL)
				first=p;
				else
				last->next=p;
				last=p;
				for(j=0;j<nob;j++)
				bit[j+start]=i;
				printf("file %s created successfully\n",fname);
				return ;
		}
		}
		else
		{
			printf("failed to create file %s\n",fname);
			return ;
		}
	}
}

void delete()
{
	NODE *p,*q;
	char fname[20];
	int i;
	printf("Enter file to be deleted ");
	scanf("%s",fname);
	
	p=q=first;
	
	while(p!=NULL)
	{
		if(strcmp(p->fname,fname)==0)
		break;
		
		q=p;
		p=q->next;
	}
	if(p==NULL)
	{
		printf("File %s not found\n",fname);
		return;
	}
	for(i=0;i<p->length;i++)
	bit[p->start+i]=0;
	if(p==first)
	first=first->next;
	else if(p==last)
	{
		last=q;
		last->next=NULL;
	}
	else
	{
	q->next=p->next;
	}
	free(p);
	printf("\n file %s deleted successfully:",fname);
}


	int main()
	{
	  int ch;
	  init();
	  while(1)
	  {
		printf("\n 1.show bit vector \n2. create new file \n3. show directory \n4. delete file \n5. exit");
	        printf("enter your choice:");
	        scanf("%d",&ch);
	        switch(ch)
		 {
		  case 1:  show_bitvector();
			   break;
		  case 2: create();
			  break;
		  case 3: show_dir();
			  break;
		  case 4: delete();
			  break;
		  case 5:exit(0);
		}
	}
		return 0;
}

2.
#include<stdio.h>
#include<stdlib.h>
int main()
{
	
	int n,rq[20], initial, totalhm, c=0, i;
	printf("\nEnter no of request:");
	scanf("%d",&n);
	printf("\n enter the request sequence:");
	for(i=0;i<n;i++)
	{
		scanf("%d",&rq[i]);
	}
	printf("\nEnter head position:");
	scanf("%d", &initial);
	while(c!=n)
	{
		int min=1000,d,index;
		for(i=0;i<n;i++)
		{
			d=abs(rq[i]-initial);
			if(min>d)
			{
				min=d;
				index=i;
			}
		}
		totalhm=totalhm+min;
		initial=rq[index];
		rq[index]=1000;
		c++;
	}
	printf("total head moment is %d",totalhm);
	return 0;
}
                             
    """)
def slip9():
    print("""
1.
#define true 1
#define false 0
#include<stdio.h>
#include<ctype.h>
int avail[4],work[10];
int max[5][4],alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3,n=5;
int i,j;
void get_alloc_state();
void print_safeseq();
void get_alloc_request();
void main()
{
get_alloc_state();
}
void get_alloc_state()
{
printf("\n Total number of resource type:%d",m);
printf("\n Total number of processes:%d",n);
int choice=0;
while(choice!=8)
{
printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Safety algorithm\n7.Resource request agorithm\n8.Exit\nEnter your choice:");
scanf("%d",&choice);
switch(choice)
{
case 1:printf("\nEnter available:");
for(j=0;j<m;j++)
{
scanf("%d",&avail[j]);
}
printf("\nEnter maximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&max[i][j]);
}
printf("\nEnter allocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
scanf("%d",&alloc[i][j]);
}
break;
case 2: printf("\nMaximum demand by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",max[i][j]);
printf("\n");
}
printf("\nAllocation by each process\n");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
printf("%d\t",alloc[i][j]);
printf("\n");
}
break;
case 3:printf("\nNeed Matrix:");
for(i=0;i<n;i++)
{
printf("Process:%d",i);
for(j=0;j<m;j++)
{
need[i][j]=max[i][j]-alloc[i][j];
printf("%4d\t",need[i][j]);
}
printf("\n");
}
break;
case 4:printf("\nAvailable:");
for(j=0;j<m;j++)
printf("%d\t",avail[j]);
break;
case 5:printf("\nRequest of process number?");
scanf("%d",&i);
printf("\nEnter request:");
for(j=0;j<m;j++)
scanf("%d",&req[i]);
break;
case 6:if(safe_state())
{
printf("\nGiven system is in safe state....");
print_safeseq();
}
break;
case 7:if(safe_state())
{
printf("\nGiven system is in safe state....");
ssi=ssi/2;
print_safeseq();
}
else
{
printf("\nGiven system is not in safe state....");
get_alloc_request();
ssi=-1;
if(safe_state())
{
printf("\nSystem will be in safe state after request....");
print_safeseq();
}
else
{
printf("\nSystem will be not in safe state after request....");
printf("\nAllocation state is undone ...");
printf("\nProcess requesting should wait....");
}
}
break;
case 8:choice=8;
break;
default:printf("Invalid Choice");
}
}
}
safe_state()
{
int found;
for(j=0;j<m;j++)
work[j]=avail[j];
for(i=0;i<n;i++)
finish[i]=false;
printf("\nCheck of safe state...");
do
{
found=false;
for(i=0;i<n;i++)
{
if(finish[i]==false && need_lte_work(i))
{
printf("\nSelected process %d",i);
finish[i]=true;
for(j=0;j<m;j++)
work[j]=work[j]+alloc[i][j];
safeseq[++ssi]=i;
found=true;
}
}
if(found==false)
{
for(i=0;i<n;i++)
if(finish[i]==false)
return(false);
return(true);
}
}while(1);
}
need_lte_work(int i)
{
for(j=0;j<m;j++)
{
if(need[i][j]>work[j])
{
return false;
}
return true;
}
}
void print_safeseq()
{
printf("\n\nSafe sequence:");
for(i=0;i<=ssi;i++)
printf("%4d",safeseq[i]);
}
void get_alloc_request()
{
if(!req_lte_need(i))
{
printf("\n Process requested more than its max claim...");
}
if(!req_lte_avail(i))
{
printf("\n Resources are not available.Pocess %d should wait..",i);
}
for(j=0;j<m;j++)
{
alloc[i][j]+=req[j];
need[i][j]-=req[j];
avail[j]-=req[j];
}
}
req_lte_need(int i)
{
for(j=0;j<m;j++)
{
if (req[j] >need[i][j])
return 0;
}
return 1;
}
req_lte_avail()
{
for(j=0; j<m; j++)
{
if(req[j]>avail[j])
return 0;
}
return 1;
}          

2.
#include<stdio.h>
#include<stdlib.h>
int main()
{
	int rq[100], i, j,n, initial, thm=0, count=0, move, size;

	printf("\nEnter no. of request: ");
	scanf("%d", &n);

	printf("\nEnter request sequence in ascending: ");
	for(i=0;i<n;i++)
		scanf("%d", &rq[i]);

	printf("\nEnter initial head position: ");
	scanf("%d", &initial);

	printf("\nEnter disk size: ");
	scanf("%d", &size);

	printf("\nEnter head movement direction for high 1 and low 0: ");
	scanf("%d", &move);

	for(i=0;i<n;i++)
	{
		for(j=0;j<n-i-1;j++)
		{
			if(rq[j]>rq[j+1])
			{
				int temp;
				temp=rq[j];
				rq[j]=rq[j+1];
				rq[j+1]=temp;
			}
		}
	}
	int index;
	for(i=0;i<n;i++)
	{
		if(initial<rq[i])
		{
			index=i;
			break;
		}
	}
	if(move==1)
	{
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	else
	{
	for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	printf("\nTotal head movement is %d \n",thm);
	return 0;
}
    """)
def slip10():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float local_sum=0;
int i;
for(i=0; i<num_elements_per_proc; i++)
{
local_sum += rand_nums[i];
}
printf("\nLocal sum for process %d-%f. avg=%f\n", world_rank, local_sum, local_sum/num_elements_per_proc);
float global_sum;
MPI_Reduce(&local_sum, &global_sum, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nTotal sum=%f.avg = %f\n", global_sum, global_sum/(world_size=num_elements_per_proc));
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}

2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		totalheadmovement += abs(size-1-0);
		initial = 0;
		
		for(i=0; i<index; i++)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i+1]-0);
			totalheadmovement += abs(size-1-0);
			initial = size-1;
		}
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}          
    """)
def slip11():
    print("""
1.
#define true 1
#define false 0
#include <stdio.h>
#include <ctype.h>
int avail[4], work[10];
int max[5][4], alloc[5][4];
int need[5][4], finish[10], req[10];
int m = 3, n = 5;
int i, j;

void main()
{
    printf("\n Total number of resource type:%d", m);
    printf("\n Total number of processes:%d", n);
    int choice = 0;
    while (choice != 8)
    {
        printf("\n 1.Accept available\n2.Display allocation and max\n3.Display the contents of need matrix\n4.Display available\n5.Accept request for a process\n6.Exit\nEnter your choice:");
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            printf("\nEnter available:");
            for (j = 0; j < m; j++)
            {
                scanf("%d", &avail[j]);
            }
            printf("\nEnter maximum demand by each process\n");
            for (i = 0; i < n; i++)
            {
                printf("Process:%d", i);
                for (j = 0; j < m; j++)
                    scanf("%d", &max[i][j]);
            }
            printf("\nEnter allocation by each process\n");
            for (i = 0; i < n; i++)
            {
                printf("Process:%d", i);
                for (j = 0; j < m; j++)
                    scanf("%d", &alloc[i][j]);
            }
            break;
        case 2:
            printf("\nMaximum demand by each process\n");
            for (i = 0; i < n; i++)
            {
                printf("Process:%d", i);
                for (j = 0; j < m; j++)
                    printf("%d\t", max[i][j]);
                printf("\n");
            }
            printf("\nAllocation by each process\n");
            for (i = 0; i < n; i++)
            {
                printf("Process:%d", i);
                for (j = 0; j < m; j++)
                    printf("%d\t", alloc[i][j]);
                printf("\n");
            }
            break;
        case 3:
            printf("\nNeed Matrix:");
            for (i = 0; i < n; i++)
            {
                printf("Process:%d", i);
                for (j = 0; j < m; j++)
                {
                    need[i][j] = max[i][j] - alloc[i][j];
                    printf("%4d\t", need[i][j]);
                }
                printf("\n");
            }
            break;
        case 4:
            printf("\nAvailable:");
            for (j = 0; j < m; j++)
                printf("%d\t", avail[j]);
            break;
        case 5:
            printf("\nRequest of process number?");
            scanf("%d", &i);
            printf("\nEnter request:");
            for (j = 0; j < m; j++)
                scanf("%d", &req[i]);
            break;
        
        case 6:
            choice = 6;
            break;
        default:
            printf("Invalid Choice");
        }
    }
}
          
2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}
    """)
def slip12():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float local_sum=0;
int i;
for(i=0; i<num_elements_per_proc; i++)
{
local_sum += rand_nums[i];
}
printf("\nLocal sum for process %d-%f. avg=%f\n", world_rank, local_sum, local_sum/num_elements_per_proc);
float global_sum;
MPI_Reduce(&local_sum, &global_sum, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nTotal sum=%f.avg = %f\n", global_sum, global_sum/(world_size=num_elements_per_proc));
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int rq[100],i,j,n,initial,thm=0,count=0,move,size;

	printf("\nEnter no. of request: ");
	scanf("%d",&n);

	printf("\nEnter request sequence: ");
	for(i=0;i<n;i++)
		scanf("%d",&rq[i]);

	printf("\nEnter initial head position: ");
	scanf("%d",&initial);

	printf("\nEnter disk size: ");
	scanf("%d", &size);

	printf("\nEnter head movement direction for high 1 and low 0: ");
	scanf("%d", &move);

	for(i=0;i<n;i++)
	{
		for(j=0;j<n-i-1;j++)
		{
			if(rq[j]>rq[j+1])
			{
				int temp;
				temp=rq[j];
				rq[j]=rq[j+1];
				rq[j+1]=temp;
			}
		}
	}
	int index;
	for(i=0;i<n;i++)
	{
		if(initial<rq[i])
		{
			index=i;
			break;
		}
	}
	if(move==1)
	{
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=0;i<index;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	else
	{
		for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=n-1;i>=index;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	printf("\nTotal head movement is %d \n",thm);
	return 0;
}
    """)
def slip13():
    print("""
1.
#define true 1
#define false 0

#include<ctype.h>
#include<stdio.h>
int avail[4],work[10];
int max[5][4];
int alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3;
int n=5;
int i,j;
void get_alloc_state();
void print_safess();
void get_alloc_request();

void main()
{
    get_alloc_state();
}

void get_alloc_state()
{
    printf("\n Total number of resource type: %d",m);
    printf("\n Total number of processes: %d",n);
    int choice = 0;
    while(choice != 8) 
    {
        printf("\n1. Accept available\n2. Display allocation and max\n ");
        printf("3. Display the contents of need matrix\n4. Display available\n ");
        printf("5. Accept request for a process\n6. Safety algorithm\n ");
        printf("7. Resources request algorithm\n8. Exit\nEnter choice : ");
        scanf("%d", &choice);
        switch(choice) 
        {
            case 1 :
                printf("\n Enter available:");
                for(j=0;j<m;j++)
                {
                    scanf("%d", &avail[j]);
                }
                printf("\n Enter maximun demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&max[i][j]);
                }
                printf("\n\n Enter allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&alloc[i][j]);
                }
                break;
            case 2 :
                printf("\n Maximum demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",max[i][j]);
                    printf("\n");
                }
                printf("\n\n Allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",alloc[i][j]);
                    printf("\n");
                }
                break;
            case 3 :
                printf("\n\n Need by each process\n");
                for(i=0;i<n; i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    {
                        need[i][j]=max[i][j]-alloc[i][j];
                        printf("%4d",need[i][j]);
                    }
                    printf("\n");
                }
                break;
            case 4 :
                printf("\nAvailable: ");
                for(j=0; j<m;j++)
                {
                    printf("%d\t",avail[j]);
                }
                break;
            case 5 :
                printf("\n\nRequest of Process number ? ");
                scanf("%d", &i);
                printf("\n Enter Request : ");
                for(j=0; j<m; j++)
                    scanf ("%d",&req[j]);
                break;
            case 6 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    ssi = ssi / 2;
                    print_safess();
                } 
                else 
                {
                    printf("\n Given system is not in safe state...");
                    get_alloc_request();
                    ssi=-1;
                    if(safe_state())
                    {
                        printf("\n system will be in safe state after request...");
                        print_safess();
                    }
                    else
                    {
                        printf("\n System will not be in safe state after request...");
                        printf("\n Allocation state is undone... ");
                        printf("\n Process requesting should wait ...");
                    }
                }
                break;
            case 7 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    print_safess();
                }
                break;
            case 8 :
                choice = 8;
                break;
            default :
                printf("Enter valid choice!");
        }
    }
}

safe_state() // safety algo
{
    int found;
    for(j=0; j<m; j++)
    work[j]=avail[j];
    for(i=0; i<n; i++)
    finish[i]=false;
    printf("\n\n Check of safe state...");
    do
    {
        found=false;
        for(i=0;i<n;i++)
        {
            if(finish[i]==false &&need_lte_work(i))
            {
                printf("\n Selected process %d",i);
                finish[i]=true;
                for (j=0;j<m;j++)
                    work[j]=work[j]+alloc[i][j];
                    safeseq[++ssi]=i;
                    found=true;
            }
        }
        if(found==false)
        {
            for(i=0;i<n;i++)
                if(finish[i]==false) 
                    return(false);
            return(true);
        }
    }while(1);
}

need_lte_work(int i)
{
    for(j=0; j<m; j++)
    {
        if(need[i][j]>work[j])
            return(false);
    }
    return(true);
}

void print_safess()
{
    printf("\n\n Safe sequence : ");
    for(i=0; i <= ssi; i++)
    printf("%4d ", safeseq[i]);
}

void get_alloc_request() // resource request algo
{
    if(!req_lte_need(i))
    {
        printf("\n Process requested more than its max claim..");
    }
    if(!req_lte_avail(i))
    {
        printf("\n Resources are not available.Process %d should wait..",i);
    }
    for(j=0;j<m; j++)
    {
        alloc[i][j]+=req[j];
        need[i][j]-=req[j];
        avail[j]-=req[j];
    }
}

req_lte_need(int i)
{
    for(j=0; j<m; j++)
    {
        if (req[j] >need[i][j])
            return 0;
    }
    return 1;
}

req_lte_avail()
{
    for(j=0; j<m; j++)
    {
        if(req[j]>avail[j])
            return 0;
    }
    return 1;
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, count=0, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		initial = size-1;
		
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(RQ[i+1]-0);
		initial = 0;
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
    """)
def slip14():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 200

typedef struct dir
{
	char fname[20];
	int start,length;
	struct dir *next;
}NODE;

NODE *first,*last;
int bit[MAX],n;
void init()
{
	int i;
	printf("Enter total no of disk blocks");
	scanf("%d",&n);
	
	for(i=0;i<10;i++)
	{
		int k=rand()%2;
		bit[k]=1;
	}
}

void show_bitvector()
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d",bit[i]);
	}
	printf("\n");
}

void show_dir()
{
	NODE *p;
	printf("File\tstart\tlength\n");
	p=first;
	while(p!=NULL)
	{
		printf("%s\t%d\t%d\n",p->fname,p->start,p->length);
		p=p->next;
	}
}

void create()
{
	NODE *p;
	char fname[20];
	int nob,i=0,j=0,start;
	printf("Enter the file name:");
	scanf("%s",fname);
	
	printf("Enter no of blocks");
	scanf("%d",&nob);

	while(1)
	{
		while(i<n)
		{	
			if(bit[i]==0)
			break;
			i++;
		}
		if(i<n)
		{
		start=i;
		j=1;
		
		while(j<nob&&i<n&&bit[i]==0)
		{
			i++;
			j++;
		}
		if(j==nob)
		{
			p=(NODE*)malloc(sizeof(NODE));
			strcpy(p->fname,fname);
			p->start=start;
			p->length=nob;
			p->next=NULL;
				if(first==NULL)
				first=p;
				else
				last->next=p;
				last=p;
				for(j=0;j<nob;j++)
				bit[j+start]=i;
				printf("file %s created successfully\n",fname);
				return ;
		}
		}
		else
		{
			printf("failed to create file %s\n",fname);
			return ;
		}
	}
}

void delete()
{
	NODE *p,*q;
	char fname[20];
	int i;
	printf("Enter file to be deleted ");
	scanf("%s",fname);
	
	p=q=first;
	
	while(p!=NULL)
	{
		if(strcmp(p->fname,fname)==0)
		break;
		
		q=p;
		p=q->next;
	}
	if(p==NULL)
	{
		printf("File %s not found\n",fname);
		return;
	}
	for(i=0;i<p->length;i++)
	bit[p->start+i]=0;
	if(p==first)
	first=first->next;
	else if(p==last)
	{
		last=q;
		last->next=NULL;
	}
	else
	{
	q->next=p->next;
	}
	free(p);
	printf("\n file %s deleted successfully:",fname);
}


	int main()
	{
	  int ch;
	  init();
	  while(1)
	  {
		printf("\n 1.show bit vector \n2. create new file \n3. show directory \n4. delete file \n5. exit");
	        printf("enter your choice:");
	        scanf("%d",&ch);
	        switch(ch)
		 {
		  case 1:  show_bitvector();
			   break;
		  case 2: create();
			  break;
		  case 3: show_dir();
			  break;
		  case 4: delete();
			  break;
		  case 5:exit(0);
		}
	}
		return 0;
}
          
2. 
#include<stdio.h>
#include<stdlib.h>
int main()
{
	
	int n,rq[20], initial, totalhm, c=0, i;
	printf("\nEnter no of request:");
	scanf("%d",&n);
	printf("\n enter the request sequence:");
	for(i=0;i<n;i++)
	{
		scanf("%d",&rq[i]);
	}
	printf("\nEnter head position:");
	scanf("%d", &initial);
	while(c!=n)
	{
		int min=1000,d,index;
		for(i=0;i<n;i++)
		{
			d=abs(rq[i]-initial);
			if(min>d)
			{
				min=d;
				index=i;
			}
		}
		totalhm=totalhm+min;
		initial=rq[index];
		rq[index]=1000;
		c++;
	}
	printf("total head moment is %d",totalhm);
	return 0;
}
           
    """)
def slip16():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 200

typedef struct dir
{
	char fname[20];
	int start,length;
	struct dir *next;
}NODE;

NODE *first,*last;
int bit[MAX],n;
void init()
{
	int i;
	printf("Enter total no of disk blocks");
	scanf("%d",&n);
	
	for(i=0;i<10;i++)
	{
		int k=rand()%2;
		bit[k]=1;
	}
}

void show_bitvector()
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d",bit[i]);
	}
	printf("\n");
}

void show_dir()
{
	NODE *p;
	printf("File\tstart\tlength\n");
	p=first;
	while(p!=NULL)
	{
		printf("%s\t%d\t%d\n",p->fname,p->start,p->length);
		p=p->next;
	}
}

void create()
{
	NODE *p;
	char fname[20];
	int nob,i=0,j=0,start;
	printf("Enter the file name:");
	scanf("%s",fname);
	
	printf("Enter no of blocks");
	scanf("%d",&nob);

	while(1)
	{
		while(i<n)
		{	
			if(bit[i]==0)
			break;
			i++;
		}
		if(i<n)
		{
		start=i;
		j=1;
		
		while(j<nob&&i<n&&bit[i]==0)
		{
			i++;
			j++;
		}
		if(j==nob)
		{
			p=(NODE*)malloc(sizeof(NODE));
			strcpy(p->fname,fname);
			p->start=start;
			p->length=nob;
			p->next=NULL;
				if(first==NULL)
				first=p;
				else
				last->next=p;
				last=p;
				for(j=0;j<nob;j++)
				bit[j+start]=i;
				printf("file %s created successfully\n",fname);
				return ;
		}
		}
		else
		{
			printf("failed to create file %s\n",fname);
			return ;
		}
	}
}

void delete()
{
	NODE *p,*q;
	char fname[20];
	int i;
	printf("Enter file to be deleted ");
	scanf("%s",fname);
	
	p=q=first;
	
	while(p!=NULL)
	{
		if(strcmp(p->fname,fname)==0)
		break;
		
		q=p;
		p=q->next;
	}
	if(p==NULL)
	{
		printf("File %s not found\n",fname);
		return;
	}
	for(i=0;i<p->length;i++)
	bit[p->start+i]=0;
	if(p==first)
	first=first->next;
	else if(p==last)
	{
		last=q;
		last->next=NULL;
	}
	else
	{
	q->next=p->next;
	}
	free(p);
	printf("\n file %s deleted successfully:",fname);
}


	int main()
	{
	  int ch;
	  init();
	  while(1)
	  {
		printf("\n 1.show bit vector \n2. create new file \n3. show directory \n4. delete file \n5. exit");
	        printf("enter your choice:");
	        scanf("%d",&ch);
	        switch(ch)
		 {
		  case 1:  show_bitvector();
			   break;
		  case 2: create();
			  break;
		  case 3: show_dir();
			  break;
		  case 4: delete();
			  break;
		  case 5:exit(0);
		}
	}
		return 0;
}
          
2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}                  
    """)
def slip18():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 200

typedef struct dir
{
	char fname[20];
	int start,length;
	struct dir *next;
}NODE;

NODE *first,*last;
int bit[MAX],n;
void init()
{
	int i;
	printf("\nEnter total no of disk blocks: ");
	scanf("%d",&n);
	
	for(i=0;i<10;i++)
	{
		int k=rand()%2;
		bit[k]=1;
	}
}

void show_bitvector()
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d",bit[i]);
	}
	printf("\n");
}

void show_dir()
{
	NODE *p;
	printf("File\tstart\tno of entries\n");
	p=first;
	while(p!=NULL)
	{
		printf("%s\t%d\t%d\n",p->fname,p->start,p->length);
		p=p->next;
	}
}

void create()
{
	NODE *p;
	char fname[20];
	int nob,i=0,j=0,start;
	printf("Enter the file name:");
	scanf("%s",fname);
	
	printf("Enter no of blocks");
	scanf("%d",&nob);

	while(1)
	{
		while(i<n)
		{	
			if(bit[i]==0)
			break;
			i++;
		}
		if(i<n)
		{
		start=i;
		j=1;
		
		while(j<nob&&i<n&&bit[i]==0)
		{
			i++;
			j++;
		}
		if(j==nob)
		{
			p=(NODE*)malloc(sizeof(NODE));
			strcpy(p->fname,fname);
			p->start=start;
			p->length=nob;
			p->next=NULL;
				if(first==NULL)
				first=p;
				else
				last->next=p;
				last=p;
				for(j=0;j<nob;j++)
				bit[j+start]=i;
				printf("file %s created successfully\n",fname);
				return ;
		}
		}
		else
		{
			printf("failed to create file %s\n",fname);
			return ;
		}
	}
}

void delete()
{
	NODE *p,*q;
	char fname[20];
	int i;
	printf("Enter file to be deleted ");
	scanf("%s",fname);
	
	p=q=first;
	
	while(p!=NULL)
	{
		if(strcmp(p->fname,fname)==0)
		break;
		
		q=p;
		p=q->next;
	}
	if(p==NULL)
	{
		printf("File %s not found\n",fname);
		return;
	}
	for(i=0;i<p->length;i++)
	bit[p->start+i]=0;
	if(p==first)
	first=first->next;
	else if(p==last)
	{
		last=q;
		last->next=NULL;
	}
	else
	{
	q->next=p->next;
	}
	free(p);
	printf("\n file %s deleted successfully:",fname);
}


int main()
{
  int ch;
  init();
  while(1)
  {
	printf("\n 1.show bit vector \n2. create new file \n3. show directory \n4. delete file \n5. exit");
        printf("\nenter your choice:");
        scanf("%d",&ch);
        switch(ch)
	 {
	  case 1:  show_bitvector();
		   break;
	  case 2: create();
		  break;
	  case 3: show_dir();
		  break;
	  case 4: delete();
		  break;
	  case 5:exit(0);
	}
	}
	return 0;
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, count=0, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		initial = size-1;
		
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(RQ[i+1]-0);
		initial = 0;
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
    """)
def slip19():
    print("""
1.
#define true 1
#define false 0

#include<ctype.h>
#include<stdio.h>
int avail[4],work[10];
int max[5][4];
int alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3;
int n=5;
int i,j;
void get_alloc_state();
void print_safess();
void get_alloc_request();

void main()
{
    get_alloc_state();
}

void get_alloc_state()
{
    printf("\n Total number of resource type: %d",m);
    printf("\n Total number of processes: %d",n);
    int choice = 0;
    while(choice != 8) 
    {
        printf("\n1. Accept available\n2. Display allocation and max\n ");
        printf("3. Display the contents of need matrix\n4. Display available\n ");
        printf("5. Accept request for a process\n6. Safety algorithm\n ");
        printf("7. Resources request algorithm\n8. Exit\nEnter choice : ");
        scanf("%d", &choice);
        switch(choice) 
        {
            case 1 :
                printf("\n Enter available:");
                for(j=0;j<m;j++)
                {
                    scanf("%d", &avail[j]);
                }
                printf("\n Enter maximun demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&max[i][j]);
                }
                printf("\n\n Enter allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&alloc[i][j]);
                }
                break;
            case 2 :
                printf("\n Maximum demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",max[i][j]);
                    printf("\n");
                }
                printf("\n\n Allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",alloc[i][j]);
                    printf("\n");
                }
                break;
            case 3 :
                printf("\n\n Need by each process\n");
                for(i=0;i<n; i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    {
                        need[i][j]=max[i][j]-alloc[i][j];
                        printf("%4d",need[i][j]);
                    }
                    printf("\n");
                }
                break;
            case 4 :
                printf("\nAvailable: ");
                for(j=0; j<m;j++)
                {
                    printf("%d\t",avail[j]);
                }
                break;
            case 5 :
                printf("\n\nRequest of Process number ? ");
                scanf("%d", &i);
                printf("\n Enter Request : ");
                for(j=0; j<m; j++)
                    scanf ("%d",&req[j]);
                break;
            case 6 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    ssi = ssi / 2;
                    print_safess();
                } 
                else 
                {
                    printf("\n Given system is not in safe state...");
                    get_alloc_request();
                    ssi=-1;
                    if(safe_state())
                    {
                        printf("\n system will be in safe state after request...");
                        print_safess();
                    }
                    else
                    {
                        printf("\n System will not be in safe state after request...");
                        printf("\n Allocation state is undone... ");
                        printf("\n Process requesting should wait ...");
                    }
                }
                break;
            case 7 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    print_safess();
                }
                break;
            case 8 :
                choice = 8;
                break;
            default :
                printf("Enter valid choice!");
        }
    }
}

safe_state() // safety algo
{
    int found;
    for(j=0; j<m; j++)
    work[j]=avail[j];
    for(i=0; i<n; i++)
    finish[i]=false;
    printf("\n\n Check of safe state...");
    do
    {
        found=false;
        for(i=0;i<n;i++)
        {
            if(finish[i]==false &&need_lte_work(i))
            {
                printf("\n Selected process %d",i);
                finish[i]=true;
                for (j=0;j<m;j++)
                    work[j]=work[j]+alloc[i][j];
                    safeseq[++ssi]=i;
                    found=true;
            }
        }
        if(found==false)
        {
            for(i=0;i<n;i++)
                if(finish[i]==false) 
                    return(false);
            return(true);
        }
    }while(1);
}

need_lte_work(int i)
{
    for(j=0; j<m; j++)
    {
        if(need[i][j]>work[j])
            return(false);
    }
    return(true);
}

void print_safess()
{
    printf("\n\n Safe sequence : ");
    for(i=0; i <= ssi; i++)
    printf("%4d ", safeseq[i]);
}

void get_alloc_request() // resource request algo
{
    if(!req_lte_need(i))
    {
        printf("\n Process requested more than its max claim..");
    }
    if(!req_lte_avail(i))
    {
        printf("\n Resources are not available.Process %d should wait..",i);
    }
    for(j=0;j<m; j++)
    {
        alloc[i][j]+=req[j];
        need[i][j]-=req[j];
        avail[j]-=req[j];
    }
}

req_lte_need(int i)
{
    for(j=0; j<m; j++)
    {
        if (req[j] >need[i][j])
            return 0;
    }
    return 1;
}

req_lte_avail()
{
    for(j=0; j<m; j++)
    {
        if(req[j]>avail[j])
            return 0;
    }
    return 1;
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		totalheadmovement += abs(size-1-0);
		initial = 0;
		
		for(i=0; i<index; i++)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i+1]-0);
			totalheadmovement += abs(size-1-0);
			initial = size-1;
		}
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
    """)
def slip20():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int RQ[100], i, n, totalheadmovement=0, initial, count=0, move, size;
	
	printf("\nEnter number of request: ");
	scanf("%d", &n);
	
	printf("\nEnter the request sequence: ");
	for(i=0; i<n; i++)
	{
		scanf("%d", &RQ[i]);
	}
	
	printf("\nEnter the initial head position: ");
	scanf("%d", &initial);
	
	printf("\nEnter the disk size: ");
	scanf("%d", &size);
	
	printf("\nEnter the initial head movement direction for high 1 and low 0: ");
	scanf("%d", &move);
	
	for(i=0; i<n; i++)
	{
		for(int j=0; j<n-i-1; j++)
		{
			if(RQ[j] > RQ[j+1])
			{
				int temp;
				temp = RQ[j];
				RQ[j] = RQ[j+1];
				RQ[j+1] = temp;
			}
		}
	}
	
	int index;
	for(i=0; i<n; i++)
	{
		if(initial < RQ[i])
		{
			index = i;
			break;
		}
	}
	
	if(move==1)
	{
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(size-RQ[i-1]-1);
		initial = size-1;
		
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i] - initial);
			initial = RQ[i];
		}
	}
	else
	{
		for(i=index-1; i>=0; i--)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
		
		totalheadmovement += abs(RQ[i+1]-0);
		initial = 0;
		
		for(i=index; i<n; i++)
		{
			totalheadmovement += abs(RQ[i]-initial);
			initial = RQ[i];
		}
	}
	
	printf("\nTotal head movement is %d", totalheadmovement);
	return 0;
}
          
2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}

    """)
def slip21():
    print("""
1.
#include<stdio.h>
#include<math.h>
int main()
{
            int queue[20],n,head,i,j,k,seek=0,max,diff;
            float avg;
            printf("Enter the max range of disk\n");
            scanf("%d",&max);
            printf("Enter the size of queue request\n");
            scanf("%d",&n);
            printf("Enter the queue of disk positions to be read\n");
            for(i=1;i<=n;i++)
            scanf("%d",&queue[i]);
            printf("Enter the initial head position\n");
            scanf("%d",&head);
            queue[0]=head;
            for(j=0;j<=n-1;j++)
            {
                        diff=abs(queue[j+1]-queue[j]);
                        seek+=diff;
                        printf("Disk head moves from %d to %d with seek %d\n",queue[j],queue[j+1],diff);
            }
            printf("Total seek time is %d\n",seek);
            avg=seek/(float)n;
            printf("Average seek time is %f\n",avg);
            return 0;
}
    
2.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
#define ARRAY_SIZE 1000
void main(int argc, char *argv[])
{
int rank, size;
int i, local_sum = 0, total_sum = 0;
int array[ARRAY_SIZE];
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);
for (i = 0; i < ARRAY_SIZE; i++)
{
array[i] = rand() % 1000;
}
for (i = 0; i < ARRAY_SIZE; i++)
{
if (array[i] % 2 == 0)
{
local_sum += array[i];
}
}
MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
if (rank == 0)
{
printf("Total sum of even numbers: %d\n", total_sum);
}
MPI_Finalize();
}

    """)
def slip22():
    print("""
1.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
void main(int argc, char *argv[])
{
int rank, size;
int i, local_sum = 0, total_sum = 0;
int array[1000];
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);
for (i = 0; i < 1000; i++)
{
array[i] = rand() % 1000;
}
for (i = 0; i < 1000; i++)
{
if (array[i] % 2 != 0)
{
local_sum += array[i];
}
}
MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
if (rank == 0)
{
printf("Total sum of odd numbers: %d\n", total_sum);
}
MPI_Finalize();
}

2.
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAX 200

typedef struct dir
{
	char fname[20];
	int start,length;
	struct dir *next;
}NODE;

NODE *first,*last;
int bit[MAX],n;
void init()
{
	int i;
	printf("Enter total no of disk blocks");
	scanf("%d",&n);
	
	for(i=0;i<10;i++)
	{
		int k=rand()%2;
		bit[k]=1;
	}
}

void show_bitvector()
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d",bit[i]);
	}
	printf("\n");
}

void show_dir()
{
	NODE *p;
	printf("File\tstart\tlength\n");
	p=first;
	while(p!=NULL)
	{
		printf("%s\t%d\t%d\n",p->fname,p->start,p->length);
		p=p->next;
	}
}

void create()
{
	NODE *p;
	char fname[20];
	int nob,i=0,j=0,start;
	printf("Enter the file name:");
	scanf("%s",fname);
	
	printf("Enter no of blocks");
	scanf("%d",&nob);

	while(1)
	{
		while(i<n)
		{	
			if(bit[i]==0)
			break;
			i++;
		}
		if(i<n)
		{
		start=i;
		j=1;
		
		while(j<nob&&i<n&&bit[i]==0)
		{
			i++;
			j++;
		}
		if(j==nob)
		{
			p=(NODE*)malloc(sizeof(NODE));
			strcpy(p->fname,fname);
			p->start=start;
			p->length=nob;
			p->next=NULL;
				if(first==NULL)
				first=p;
				else
				last->next=p;
				last=p;
				for(j=0;j<nob;j++)
				bit[j+start]=i;
				printf("file %s created successfully\n",fname);
				return ;
		}
		}
		else
		{
			printf("failed to create file %s\n",fname);
			return ;
		}
	}
}

void delete()
{
	NODE *p,*q;
	char fname[20];
	int i;
	printf("Enter file to be deleted ");
	scanf("%s",fname);
	
	p=q=first;
	
	while(p!=NULL)
	{
		if(strcmp(p->fname,fname)==0)
		break;
		
		q=p;
		p=q->next;
	}
	if(p==NULL)
	{
		printf("File %s not found\n",fname);
		return;
	}
	for(i=0;i<p->length;i++)
	bit[p->start+i]=0;
	if(p==first)
	first=first->next;
	else if(p==last)
	{
		last=q;
		last->next=NULL;
	}
	else
	{
	q->next=p->next;
	}
	free(p);
	printf("\n file %s deleted successfully:",fname);
}


	int main()
	{
	  int ch;
	  init();
	  while(1)
	  {
		printf("\n 1.show bit vector \n2. create new file \n3. show directory \n4. delete file \n5. exit");
	        printf("enter your choice:");
	        scanf("%d",&ch);
	        switch(ch)
		 {
		  case 1:  show_bitvector();
			   break;
		  case 2: create();
			  break;
		  case 3: show_dir();
			  break;
		  case 4: delete();
			  break;
		  case 5:exit(0);
		}
	}
		return 0;
}
          

    """)
def slip23():
    print("""
1.
#define true 1
#define false 0

#include<ctype.h>
#include<stdio.h>
int avail[4],work[10];
int max[5][4];
int alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3;
int n=5;
int i,j;
void get_alloc_state();
void print_safess();
void get_alloc_request();

void main()
{
    get_alloc_state();
}

void get_alloc_state()
{
    printf("\n Total number of resource type: %d",m);
    printf("\n Total number of processes: %d",n);
    int choice = 0;
    while(choice != 8) 
    {
        printf("\n1. Accept available\n2. Display allocation and max\n ");
        printf("3. Display the contents of need matrix\n4. Display available\n ");
        printf("5. Accept request for a process\n6. Safety algorithm\n ");
        printf("7. Resources request algorithm\n8. Exit\nEnter choice : ");
        scanf("%d", &choice);
        switch(choice) 
        {
            case 1 :
                printf("\n Enter available:");
                for(j=0;j<m;j++)
                {
                    scanf("%d", &avail[j]);
                }
                printf("\n Enter maximun demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&max[i][j]);
                }
                printf("\n\n Enter allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&alloc[i][j]);
                }
                break;
            case 2 :
                printf("\n Maximum demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",max[i][j]);
                    printf("\n");
                }
                printf("\n\n Allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",alloc[i][j]);
                    printf("\n");
                }
                break;
            case 3 :
                printf("\n\n Need by each process\n");
                for(i=0;i<n; i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    {
                        need[i][j]=max[i][j]-alloc[i][j];
                        printf("%4d",need[i][j]);
                    }
                    printf("\n");
                }
                break;
            case 4 :
                printf("\nAvailable: ");
                for(j=0; j<m;j++)
                {
                    printf("%d\t",avail[j]);
                }
                break;
            case 5 :
                printf("\n\nRequest of Process number ? ");
                scanf("%d", &i);
                printf("\n Enter Request : ");
                for(j=0; j<m; j++)
                    scanf ("%d",&req[j]);
                break;
            case 6 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    ssi = ssi / 2;
                    print_safess();
                } 
                else 
                {
                    printf("\n Given system is not in safe state...");
                    get_alloc_request();
                    ssi=-1;
                    if(safe_state())
                    {
                        printf("\n system will be in safe state after request...");
                        print_safess();
                    }
                    else
                    {
                        printf("\n System will not be in safe state after request...");
                        printf("\n Allocation state is undone... ");
                        printf("\n Process requesting should wait ...");
                    }
                }
                break;
            case 7 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    print_safess();
                }
                break;
            case 8 :
                choice = 8;
                break;
            default :
                printf("Enter valid choice!");
        }
    }
}

safe_state() // safety algo
{
    int found;
    for(j=0; j<m; j++)
    work[j]=avail[j];
    for(i=0; i<n; i++)
    finish[i]=false;
    printf("\n\n Check of safe state...");
    do
    {
        found=false;
        for(i=0;i<n;i++)
        {
            if(finish[i]==false &&need_lte_work(i))
            {
                printf("\n Selected process %d",i);
                finish[i]=true;
                for (j=0;j<m;j++)
                    work[j]=work[j]+alloc[i][j];
                    safeseq[++ssi]=i;
                    found=true;
            }
        }
        if(found==false)
        {
            for(i=0;i<n;i++)
                if(finish[i]==false) 
                    return(false);
            return(true);
        }
    }while(1);
}

need_lte_work(int i)
{
    for(j=0; j<m; j++)
    {
        if(need[i][j]>work[j])
            return(false);
    }
    return(true);
}

void print_safess()
{
    printf("\n\n Safe sequence : ");
    for(i=0; i <= ssi; i++)
    printf("%4d ", safeseq[i]);
}

void get_alloc_request() // resource request algo
{
    if(!req_lte_need(i))
    {
        printf("\n Process requested more than its max claim..");
    }
    if(!req_lte_avail(i))
    {
        printf("\n Resources are not available.Process %d should wait..",i);
    }
    for(j=0;j<m; j++)
    {
        alloc[i][j]+=req[j];
        need[i][j]-=req[j];
        avail[j]-=req[j];
    }
}

req_lte_need(int i)
{
    for(j=0; j<m; j++)
    {
        if (req[j] >need[i][j])
            return 0;
    }
    return 1;
}

req_lte_avail()
{
    for(j=0; j<m; j++)
    {
        if(req[j]>avail[j])
            return 0;
    }
    return 1;
}         

2.
#include<stdio.h>
#include<stdlib.h>
int main()
{
	
	int n,rq[20], initial, totalhm, c=0, i;
	printf("\nEnter no of request:");
	scanf("%d",&n);
	printf("\n enter the request sequence:");
	for(i=0;i<n;i++)
	{
		scanf("%d",&rq[i]);
	}
	printf("\nEnter head position:");
	scanf("%d", &initial);
	while(c!=n)
	{
		int min=1000,d,index;
		for(i=0;i<n;i++)
		{
			d=abs(rq[i]-initial);
			if(min>d)
			{
				min=d;
				index=i;
			}
		}
		totalhm=totalhm+min;
		initial=rq[index];
		rq[index]=1000;
		c++;
	}
	printf("total head moment is %d",totalhm);
	return 0;
}

    """)
def slip24():
    print("""
1.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
void main(int argc, char *argv[])
{
int rank, size;
int i, local_sum = 0, total_sum = 0;
int array[1000];
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);
for (i = 0; i < 1000; i++)
{
array[i] = rand() % 1000;
}
for (i = 0; i < 1000; i++)
{
if (array[i] % 2 != 0)
{
local_sum += array[i];
}
}
MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
if (rank == 0)
{
printf("Total sum of odd numbers: %d\n", total_sum);
}
MPI_Finalize();
}

2.
#define true 1
#define false 0

#include<ctype.h>
#include<stdio.h>
int avail[4],work[10];
int max[5][4];
int alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3;
int n=5;
int i,j;
void get_alloc_state();
void print_safess();
void get_alloc_request();

void main()
{
    get_alloc_state();
}

void get_alloc_state()
{
    printf("\n Total number of resource type: %d",m);
    printf("\n Total number of processes: %d",n);
    int choice = 0;
    while(choice != 8) 
    {
        printf("\n1. Accept available\n2. Display allocation and max\n ");
        printf("3. Display the contents of need matrix\n4. Display available\n ");
        printf("5. Accept request for a process\n6. Safety algorithm\n ");
        printf("7. Resources request algorithm\n8. Exit\nEnter choice : ");
        scanf("%d", &choice);
        switch(choice) 
        {
            case 1 :
                printf("\n Enter available:");
                for(j=0;j<m;j++)
                {
                    scanf("%d", &avail[j]);
                }
                printf("\n Enter maximun demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&max[i][j]);
                }
                printf("\n\n Enter allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&alloc[i][j]);
                }
                break;
            case 2 :
                printf("\n Maximum demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",max[i][j]);
                    printf("\n");
                }
                printf("\n\n Allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",alloc[i][j]);
                    printf("\n");
                }
                break;
            case 3 :
                printf("\n\n Need by each process\n");
                for(i=0;i<n; i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    {
                        need[i][j]=max[i][j]-alloc[i][j];
                        printf("%4d",need[i][j]);
                    }
                    printf("\n");
                }
                break;
            case 4 :
                printf("\nAvailable: ");
                for(j=0; j<m;j++)
                {
                    printf("%d\t",avail[j]);
                }
                break;
            case 5 :
                printf("\n\nRequest of Process number ? ");
                scanf("%d", &i);
                printf("\n Enter Request : ");
                for(j=0; j<m; j++)
                    scanf ("%d",&req[j]);
                break;
            case 6 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    ssi = ssi / 2;
                    print_safess();
                } 
                else 
                {
                    printf("\n Given system is not in safe state...");
                    get_alloc_request();
                    ssi=-1;
                    if(safe_state())
                    {
                        printf("\n system will be in safe state after request...");
                        print_safess();
                    }
                    else
                    {
                        printf("\n System will not be in safe state after request...");
                        printf("\n Allocation state is undone... ");
                        printf("\n Process requesting should wait ...");
                    }
                }
                break;
            case 7 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    print_safess();
                }
                break;
            case 8 :
                choice = 8;
                break;
            default :
                printf("Enter valid choice!");
        }
    }
}

safe_state() // safety algo
{
    int found;
    for(j=0; j<m; j++)
    work[j]=avail[j];
    for(i=0; i<n; i++)
    finish[i]=false;
    printf("\n\n Check of safe state...");
    do
    {
        found=false;
        for(i=0;i<n;i++)
        {
            if(finish[i]==false &&need_lte_work(i))
            {
                printf("\n Selected process %d",i);
                finish[i]=true;
                for (j=0;j<m;j++)
                    work[j]=work[j]+alloc[i][j];
                    safeseq[++ssi]=i;
                    found=true;
            }
        }
        if(found==false)
        {
            for(i=0;i<n;i++)
                if(finish[i]==false) 
                    return(false);
            return(true);
        }
    }while(1);
}

need_lte_work(int i)
{
    for(j=0; j<m; j++)
    {
        if(need[i][j]>work[j])
            return(false);
    }
    return(true);
}

void print_safess()
{
    printf("\n\n Safe sequence : ");
    for(i=0; i <= ssi; i++)
    printf("%4d ", safeseq[i]);
}

void get_alloc_request() // resource request algo
{
    if(!req_lte_need(i))
    {
        printf("\n Process requested more than its max claim..");
    }
    if(!req_lte_avail(i))
    {
        printf("\n Resources are not available.Process %d should wait..",i);
    }
    for(j=0;j<m; j++)
    {
        alloc[i][j]+=req[j];
        need[i][j]-=req[j];
        avail[j]-=req[j];
    }
}

req_lte_need(int i)
{
    for(j=0; j<m; j++)
    {
        if (req[j] >need[i][j])
            return 0;
    }
    return 1;
}

req_lte_avail()
{
    for(j=0; j<m; j++)
    {
        if(req[j]>avail[j])
            return 0;
    }
    return 1;
}
    """)
def slip26():
    print("""
1.
#define true 1
#define false 0

#include<ctype.h>
#include<stdio.h>
int avail[4],work[10];
int max[5][4];
int alloc[5][4];
int need[5][4],finish[10],req[10];
int safeseq[10],ssi=-1;
int m=3;
int n=5;
int i,j;
void get_alloc_state();
void print_safess();
void get_alloc_request();

void main()
{
    get_alloc_state();
}

void get_alloc_state()
{
    printf("\n Total number of resource type: %d",m);
    printf("\n Total number of processes: %d",n);
    int choice = 0;
    while(choice != 8) 
    {
        printf("\n1. Accept available\n2. Display allocation and max\n ");
        printf("3. Display the contents of need matrix\n4. Display available\n ");
        printf("5. Accept request for a process\n6. Safety algorithm\n ");
        printf("7. Resources request algorithm\n8. Exit\nEnter choice : ");
        scanf("%d", &choice);
        switch(choice) 
        {
            case 1 :
                printf("\n Enter available:");
                for(j=0;j<m;j++)
                {
                    scanf("%d", &avail[j]);
                }
                printf("\n Enter maximun demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&max[i][j]);
                }
                printf("\n\n Enter allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    scanf("%d",&alloc[i][j]);
                }
                break;
            case 2 :
                printf("\n Maximum demand by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",max[i][j]);
                    printf("\n");
                }
                printf("\n\n Allocation by each process\n");
                for(i=0;i<n;i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    printf("%d\t",alloc[i][j]);
                    printf("\n");
                }
                break;
            case 3 :
                printf("\n\n Need by each process\n");
                for(i=0;i<n; i++)
                {
                    printf("Process %d: ",i);
                    for(j=0;j<m;j++)
                    {
                        need[i][j]=max[i][j]-alloc[i][j];
                        printf("%4d",need[i][j]);
                    }
                    printf("\n");
                }
                break;
            case 4 :
                printf("\nAvailable: ");
                for(j=0; j<m;j++)
                {
                    printf("%d\t",avail[j]);
                }
                break;
            case 5 :
                printf("\n\nRequest of Process number ? ");
                scanf("%d", &i);
                printf("\n Enter Request : ");
                for(j=0; j<m; j++)
                    scanf ("%d",&req[j]);
                break;
            case 6 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    ssi = ssi / 2;
                    print_safess();
                } 
                else 
                {
                    printf("\n Given system is not in safe state...");
                    get_alloc_request();
                    ssi=-1;
                    if(safe_state())
                    {
                        printf("\n system will be in safe state after request...");
                        print_safess();
                    }
                    else
                    {
                        printf("\n System will not be in safe state after request...");
                        printf("\n Allocation state is undone... ");
                        printf("\n Process requesting should wait ...");
                    }
                }
                break;
            case 7 :
                if(safe_state()) 
                {
                    printf("\n Given system is in safe state...");
                    print_safess();
                }
                break;
            case 8 :
                choice = 8;
                break;
            default :
                printf("Enter valid choice!");
        }
    }
}

safe_state() // safety algo
{
    int found;
    for(j=0; j<m; j++)
    work[j]=avail[j];
    for(i=0; i<n; i++)
    finish[i]=false;
    printf("\n\n Check of safe state...");
    do
    {
        found=false;
        for(i=0;i<n;i++)
        {
            if(finish[i]==false &&need_lte_work(i))
            {
                printf("\n Selected process %d",i);
                finish[i]=true;
                for (j=0;j<m;j++)
                    work[j]=work[j]+alloc[i][j];
                    safeseq[++ssi]=i;
                    found=true;
            }
        }
        if(found==false)
        {
            for(i=0;i<n;i++)
                if(finish[i]==false) 
                    return(false);
            return(true);
        }
    }while(1);
}

need_lte_work(int i)
{
    for(j=0; j<m; j++)
    {
        if(need[i][j]>work[j])
            return(false);
    }
    return(true);
}

void print_safess()
{
    printf("\n\n Safe sequence : ");
    for(i=0; i <= ssi; i++)
    printf("%4d ", safeseq[i]);
}

void get_alloc_request() // resource request algo
{
    if(!req_lte_need(i))
    {
        printf("\n Process requested more than its max claim..");
    }
    if(!req_lte_avail(i))
    {
        printf("\n Resources are not available.Process %d should wait..",i);
    }
    for(j=0;j<m; j++)
    {
        alloc[i][j]+=req[j];
        need[i][j]-=req[j];
        avail[j]-=req[j];
    }
}

req_lte_need(int i)
{
    for(j=0; j<m; j++)
    {
        if (req[j] >need[i][j])
            return 0;
    }
    return 1;
}

req_lte_avail()
{
    for(j=0; j<m; j++)
    {
        if(req[j]>avail[j])
            return 0;
    }
    return 1;
}
          
2.
#include<stdio.h>
#include<math.h>
int main()
{
            int queue[20],n,head,i,j,k,seek=0,max,diff;
            float avg;
            printf("Enter the max range of disk\n");
            scanf("%d",&max);
            printf("Enter the size of queue request\n");
            scanf("%d",&n);
            printf("Enter the queue of disk positions to be read\n");
            for(i=1;i<=n;i++)
            scanf("%d",&queue[i]);
            printf("Enter the initial head position\n");
            scanf("%d",&head);
            queue[0]=head;
            for(j=0;j<=n-1;j++)
            {
                        diff=abs(queue[j+1]-queue[j]);
                        seek+=diff;
                        printf("Disk head moves from %d to %d with seek %d\n",queue[j],queue[j+1],diff);
            }
            printf("Total seek time is %d\n",seek);
            avg=seek/(float)n;
            printf("Average seek time is %f\n",avg);
            return 0;
}
    """)
def slip27():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
int main()
{
	int rq[100], i, j,n, initial, thm=0, count=0, move, size;

	printf("\nEnter no. of request: ");
	scanf("%d", &n);

	printf("\nEnter request sequence in ascending: ");
	for(i=0;i<n;i++)
		scanf("%d", &rq[i]);

	printf("\nEnter initial head position: ");
	scanf("%d", &initial);

	printf("\nEnter disk size: ");
	scanf("%d", &size);

	printf("\nEnter head movement direction for high 1 and low 0: ");
	scanf("%d", &move);

	for(i=0;i<n;i++)
	{
		for(j=0;j<n-i-1;j++)
		{
			if(rq[j]>rq[j+1])
			{
				int temp;
				temp=rq[j];
				rq[j]=rq[j+1];
				rq[j+1]=temp;
			}
		}
	}
	int index;
	for(i=0;i<n;i++)
	{
		if(initial<rq[i])
		{
			index=i;
			break;
		}
	}
	if(move==1)
	{
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	else
	{
	for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	printf("\nTotal head movement is %d \n",thm);
	return 0;
}

2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}
    """)
def slip28():
    print("""
1
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int rq[100],i,j,n,initial,thm=0,count=0,move,size;

	printf("\nEnter no. of request: ");
	scanf("%d",&n);

	printf("\nEnter request sequence: ");
	for(i=0;i<n;i++)
		scanf("%d",&rq[i]);

	printf("\nEnter initial head position: ");
	scanf("%d",&initial);

	printf("\nEnter disk size: ");
	scanf("%d", &size);

	printf("\nEnter head movement direction for high 1 and low 0: ");
	scanf("%d", &move);

	for(i=0;i<n;i++)
	{
		for(j=0;j<n-i-1;j++)
		{
			if(rq[j]>rq[j+1])
			{
				int temp;
				temp=rq[j];
				rq[j]=rq[j+1];
				rq[j+1]=temp;
			}
		}
	}
	int index;
	for(i=0;i<n;i++)
	{
		if(initial<rq[i])
		{
			index=i;
			break;
		}
	}
	if(move==1)
	{
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=0;i<index;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	else
	{
		for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=n-1;i>=index;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	printf("\nTotal head movement is %d \n",thm);
	return 0;
}

2.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float local_sum=0;
int i;
for(i=0; i<num_elements_per_proc; i++)
{
local_sum += rand_nums[i];
}
printf("\nLocal sum for process %d-%f. avg=%f\n", world_rank, local_sum, local_sum/num_elements_per_proc);
float global_sum;
MPI_Reduce(&local_sum, &global_sum, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nTotal sum=%f.avg = %f\n", global_sum, global_sum/(world_size=num_elements_per_proc));
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}
    """)
def slip29():
    print("""
1.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
#define ARRAY_SIZE 1000
void main(int argc, char *argv[])
{
int rank, size;
int i, local_sum = 0, total_sum = 0;
int array[ARRAY_SIZE];
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);
for (i = 0; i < ARRAY_SIZE; i++)
{
array[i] = rand() % 1000;
}
for (i = 0; i < ARRAY_SIZE; i++)
{
if (array[i] % 2 == 0)
{
local_sum += array[i];
}
}
MPI_Reduce(&local_sum, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
if (rank == 0)
{
printf("Total sum of even numbers: %d\n", total_sum);
}
MPI_Finalize();
}
          
2.
#include<stdio.h>
#include<stdlib.h>

int main()
{
	int rq[100],i,j,n,initial,thm=0,count=0,move,size;

	printf("\nEnter no. of request: ");
	scanf("%d",&n);

	printf("\nEnter request sequence: ");
	for(i=0;i<n;i++)
		scanf("%d",&rq[i]);

	printf("\nEnter initial head position: ");
	scanf("%d",&initial);

	printf("\nEnter disk size: ");
	scanf("%d", &size);

	printf("\nEnter head movement direction for high 1 and low 0: ");
	scanf("%d", &move);

	for(i=0;i<n;i++)
	{
		for(j=0;j<n-i-1;j++)
		{
			if(rq[j]>rq[j+1])
			{
				int temp;
				temp=rq[j];
				rq[j]=rq[j+1];
				rq[j+1]=temp;
			}
		}
	}
	int index;
	for(i=0;i<n;i++)
	{
		if(initial<rq[i])
		{
			index=i;
			break;
		}
	}
	if(move==1)
	{
		for(i=index;i<n;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=0;i<index;i++)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	else
	{
		for(i=index-1;i>=0;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
		for(i=n-1;i>=index;i--)
		{
			thm=thm+abs(rq[i]-initial);
			initial=rq[i];
		}
	}
	printf("\nTotal head movement is %d \n",thm);
	return 0;
}
    """)
def slip30():
    print("""
1.
#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<assert.h>
#include<time.h>
float *create_rand_nums(int num_elements)
{
int i;
float *rand_nums =(float*)malloc(sizeof(float)*num_elements);
assert(rand_nums!=NULL);
for(i=0; i<num_elements; i++)
{
rand_nums[i] = (rand()/(float)RAND_MAX);
}
return rand_nums;
}
int main(int argc, char**argv)
{
if(argc!=2)
{
fprintf(stderr, "Usage: avg num_elements_per_proc\n");
exit(1);
}
int num_elements_per_proc = atoi(argv[1]);
MPI_Init(NULL, NULL);
int world_rank;
MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
int world_size;
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
srand(time(NULL)*world_rank);
float *rand_nums = NULL;
rand_nums = create_rand_nums(num_elements_per_proc);
float max=0;
int k;
for(k=0; k<num_elements_per_proc; k++)
{
if(rand_nums[k]>max)
max = rand_nums[k];
}
float global_max;
MPI_Reduce(&max, &global_max, 1, MPI_FLOAT, MPI_MAX, 0, MPI_COMM_WORLD);
float min=999;
int z;
for(z=0; z<num_elements_per_proc; z++)
{
if(rand_nums[z]<min)
{
min = rand_nums[z];
}
}
float global_min;
MPI_Reduce(&min, &global_min, 1, MPI_FLOAT, MPI_MIN, 0, MPI_COMM_WORLD);
if(world_rank==0)
{
printf("\nMax is %f\n", global_max);
printf("\nMin is %f\n", global_min);
}
free(rand_nums);
MPI_Barrier(MPI_COMM_WORLD);
MPI_Finalize();
}

2.
#include<stdio.h>
#include<math.h>
int main()
{
            int queue[20],n,head,i,j,k,seek=0,max,diff;
            float avg;
            printf("Enter the max range of disk\n");
            scanf("%d",&max);
            printf("Enter the size of queue request\n");
            scanf("%d",&n);
            printf("Enter the queue of disk positions to be read\n");
            for(i=1;i<=n;i++)
            scanf("%d",&queue[i]);
            printf("Enter the initial head position\n");
            scanf("%d",&head);
            queue[0]=head;
            for(j=0;j<=n-1;j++)
            {
                        diff=abs(queue[j+1]-queue[j]);
                        seek+=diff;
                        printf("Disk head moves from %d to %d with seek %d\n",queue[j],queue[j+1],diff);
            }
            printf("Total seek time is %d\n",seek);
            avg=seek/(float)n;
            printf("Average seek time is %f\n",avg);
            return 0;
}
    """)