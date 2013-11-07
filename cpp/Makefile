CXX := g++
CXXFLAGS := -g -O2 -Wall
BINS := vsm_text_unittest to_vsm

all: $(BINS)
vsm_text.o: vsm_text.cc
	 $(CXX) $(CXXFLAGS) -c  vsm_text.cc -m64  -DOS_LINUX -o vsm_text.o
vsm_text_unittest.o: vsm_text_unittest.cc 
	 $(CXX) $(CXXFLAGS) -c vsm_text_unittest.cc -m64  -DOS_LINUX -o vsm_text_unittest.o
vsm_text_unittest: vsm_text_unittest.o vsm_text.o
	 $(CXX) $(CXXFLAGS) vsm_text_unittest.o vsm_text.o libICTCLAS50.a -o vsm_text_unittest
to_vsm: to_vsm.cc vsm_text.o
	 $(CXX) $(CXXFLAGS) to_vsm.cc  vsm_text.o libICTCLAS50.a -o to_vsm

clean:
	rm $(BINS) *.o
