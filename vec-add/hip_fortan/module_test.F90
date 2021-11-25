module test
 use cudafor
 implicit none
 integer, parameter :: singtype = selected_real_kind(6,37)    ! single precision
 integer, parameter :: doubtype = selected_real_kind(15,307)  ! double precision
 
 integer, parameter :: mykind    = doubtype
 real(mykind), parameter :: tol_iter = 0.000000001_mykind

 real(mykind), dimension(:), allocatable  :: x,y
 real(mykind) :: a

 real(mykind), dimension(:), device, allocatable  :: x_d,y_d

 integer, parameter :: N = 4000

 integer :: iermpi, iercuda

end module
  
