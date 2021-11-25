
module vecadd_mod

  contains

subroutine vecadd
   use test 
   implicit none
  
   integer :: i
    type(dim3) :: grid, tBlock

  tBlock = dim3(256,1,1)
  grid = dim3(ceiling(real(N)/tBlock%x),1,1)
  
   !$cuf kernel do(1) <<<grid,tBlock>>>
   do i=1,size(y_d,1)
    y_d(i) = y_d(i) + a 
   end do
  
end subroutine

end module
