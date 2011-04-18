#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," HH_traub.mod");
    fprintf(stderr," IM_cortex.mod");
    fprintf(stderr, "\n");
  }
  _HH_traub_reg();
  _IM_cortex_reg();
}
