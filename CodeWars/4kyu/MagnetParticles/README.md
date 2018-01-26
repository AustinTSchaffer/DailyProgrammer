$$v(k,n) = \frac{1}{k(n+1)^{2k}}$$

$$u(1,N) = \sum_{n=1}^{N}{v(1,n)} = \frac{1}{1*2^2} + \frac{1}{1*3^2} + ... + \frac{1}{1*(N+1)^2}$$

$$S(K,N) = \sum_{k=1}^{K}{u(k,N)} = \sum_{k=1}^{K}{(\sum_{n=1}^{N}{v(k,n)})}$$

Write a C# function that does that last function. 
