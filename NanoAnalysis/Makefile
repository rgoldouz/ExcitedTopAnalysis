ROOTCFLAGS     = $(shell root-config --cflags)
ROOTLIBS       = $(shell root-config --libs)
ROOTGLIBS      = $(shell root-config --glibs) 
CORLIBS        = lib/libcorrectionlib.so
CORFLAGS       = $(shell correction config --cflags)

CVMA            = /cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_4_0/src/
BOOST          = /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/boost/1.67.0/include/
INCLUDES       = -I./include -I$(BOOST) -I$(CVMA) 

CXX            = g++ -m64
CXXFLAGS       = -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2  $(INCLUDES) 
CXXFLAGS      += $(ROOTCFLAGS)

LD             = g++ -m64
LDFLAGS        =


SOFLAGS        = -O -shared  -fPIC #-flat_namespace 
LIBS           = $(ROOTLIBS) 

GLIBS         = $(ROOTGLIBS) -lMinuit -lMinuit2 -lTreePlayer -lGenVector -lTMVA

SRCS = src/ScaleFactors.cc src/GEScaleSyst.cc src/Utils.cc src/BTagCalibrationStandalone.cc src/RoccoR.cc src/lepton_candidate.cc src/jet_candidate.cc src/PU_reWeighting.cc src/sumOfWeights.cc  src/MyAnalysis.cc 
OBJS =  $(patsubst %.C,%.o,$(SRCS:.cc=.o))

LIB=lib/libmain.so


.SUFFIXES: .cc,.C,.hh,.h

# Rules ====================================
all: $(LIB)  bin/RunAll

lib : $(LIB)
$(LIB): $(OBJS)
	@echo "Creating library $(LIB)"
	mkdir -p lib
	$(PYPATH)
	$(LD) $(LDFLAGS) $(GLIBS) $(SOFLAGS) $(OBJS) -o $(LIB)
	@echo "$(LIB) successfully compiled!"

bin/RunAll : src/main.C  $(LIB)
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -ldl -L./lib -lCondFormatsJetMETObjects -lCondFormatsSerialization -lcorrectionlib -lEFTGenReaderEFTHelperUtilities -lmain src/main.C $(GLIBS) -o $@

clean:
	$(RM) $(OBJS)	
	$(RM) $(LIB)
	$(RM) bin/RunAll

purge:
	$(RM) $(OBJS)

deps: $(SRCS)
	makedepend $(INCLUDES) $^

# DO NOT DELETE THIS LINE -- make depend needs it
