subroutine vecadd
 use test
 implicit none

 integer :: i

 !$cuf kernel do(1) <<<*,*>>>
 do i=1,size(y_d,1)
  y_d(i) = y_d(i) + x_d(i)*a 
 end do

end subroutine
