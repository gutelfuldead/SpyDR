#include <stdio.h>
#include <sys/socket.h>

void main() {

int n;
unsigned int m = sizeof(n);
int fdsocket;
fdsocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP); // example
getsockopt(fdsocket,SOL_SOCKET,SO_RCVBUF,(void *)&n, &m);
// now the variable n will have the socket size
printf("%d",n)
}
