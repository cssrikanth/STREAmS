program main
  use test
  implicit none
  
  allocate(x(N),y(N))
  allocate(x_d(N),y_d(N))

  x = 1.0_mykind
  y = 2.0_mykind
  a = 2.0_mykind

  x_d = x
  y_d = y

  call vecadd() 


end program
