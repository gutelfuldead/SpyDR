#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/time.h>
#include <stdlib.h>
#include <memory.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <stdarg.h>
/* the next two includes probably aren't relevant for you, but I typically use them all anyway */
#include <math.h>
#include <sys/termios.h>

void main()
{
  int n;
  unsigned int m = sizeof(n);
  int fdsocket;
  fdsocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP); // example
  getsockopt(fdsocket,SOL_SOCKET,SO_RCVBUF,(void *)&n, &m);
  // now the variable n will have the socket size
  printf("max size of socket in bytes: %d\n",n);
}
