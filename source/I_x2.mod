TITLE Cortical I xx subthreshold current 
:
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX ixx
	USEION k READ ek WRITE ik
        	RANGE gkbar, m_inf
	GLOBAL taumax

}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}


PARAMETER {
	v		(mV)
	celsius 	= 36    	(degC)
	ek	= -50	(mV)
	ekk	= -65	(mV)
	gkbar	= - 5e-6	(mho/cm2)
	taumax	= 10	(ms)		: peak value of tau
	tau_m	= 1	(ms)
}



STATE {
	m
}

ASSIGNED {
	ik	(mA/cm2)
	m_inf
	tau_peak	(ms)
	tadj
}

BREAKPOINT {
	SOLVE states METHOD euler
	ik = gkbar * ((v - ekk)^2)
}

DERIVATIVE states { 
	evaluate_fct(v)

	m' = (m_inf - m) / tau_m
}

UNITSOFF
INITIAL {
	evaluate_fct(v)
	m = 0
:
:  The Q10 value is assumed to be 2.3
:
        tadj = 2.3 ^ ((celsius-36)/10)
	tau_peak = taumax / tadj
}

PROCEDURE evaluate_fct(v(mV)) {

	m_inf = exptable(v)
}
UNITSON


FUNCTION exptable(x) { 
	TABLE  FROM -200 TO 25 WITH 10000

	if ((x > -40)) {
		exptable = 0.
	} else {
		exptable = -1*(1 - (1 / (1+ exp((x + 50)/5))))
	}
}
