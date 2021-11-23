include rules.mk

TEST_SRC = mod_test.F90
TEST_NAME = $(TEST_SRC:.F90=)
.PHONY: build.hip codegen.hip clean

codegen.hip:
	gpufort -w $(TEST_SRC) -E hip --config-file options.py.in
	#gpufort -w  main.F90 -E hip --config-file options.py.in 
	#gpufort -w vec-add.F90 -E hip --config-file options.py.in --emit-cpu-impl --emit-debug-code
build.hip: codegen.hip
	$(HIPCC) $(HIPCC_CFLAGS) -c $(TEST_SRC)-fort2hip.hip.cpp
	$(HIPFC) $(TEST_SRC)-gpufort.f08 -o $(TEST_NAME) $(TEST_SRC)-fort2hip.hip.o $(CFLAGS)

clean:
	rm -rf *-gpufort.* *-fort2hip.* *.o *.mod gpufort*.h $(TEST_NAME) *.gpufort_mod log/
