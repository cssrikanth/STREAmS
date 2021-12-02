include rules.mk

.PHONY: build.hip codegen.hip link.hip clean

codegen.hip:
	gpufort -w mod_streams.F90 -E hip --config-file options.py.in 
	gpufort -w alloc.F90 -E hip --config-file options.py.in 
	gpufort -w bcdf.F90 -E hip --config-file options.py.in 
	#gpufort -w combined.F90 -E hip --config-file options.py.in
build.hip: 
	$(HIPCC) $(HIPCC_CFLAGS) -c mod_bcdf-fort2hip.hip.cpp
	$(HIPFC) mod_streams.F90-gpufort.f08 -c $(CFLAGS)
	$(HIPFC) bcdf.F90-gpufort.f08 -c  $(CFLAGS)
	#$(HIPFC) combined.F90-gpufort.f08 -c  $(CFLAGS)
	
link.hip:
	$(HIPFC)  -o final combined.F90-gpufort.o  kernel.F90-gpufort.o  module_test.F90-gpufort.o  vecadd_mod-fort2hip.hip.o $(CFLAGS)
	

clean:
	rm -rf options.py.in *.F90 *-gpufort.* *-fort2hip.* *.o *.mod gpufort*.h $(TEST_NAME) *.gpufort_mod log/
