FC     ?= gfortran
CFLAGS ?= $(shell gpufort --gfortran_config)

HIPCC ?= hipcc -fPIC 
HIPCC += -DGPUFORT_PRINT_KERNEL_ARGS_ALL 
#HIPCC += -DGPUFORT_PRINT_INPUT_ARRAY_NORMS_ALL
#HIPCC += -DGPUFORT_PRINT_OUTPUT_ARRAY_NORMS_ALL
HIPCC += -DGPUFORT_PRINT_INPUT_ARRAYS_ALL
HIPCC += -DGPUFORT_PRINT_OUTPUT_ARRAYS_ALL
HIPFC ?= hipfc

HIPCC_CFLAGS ?= $(shell gpufort --cpp_config)
