TITLE Cortical I x  subthreshold current
:
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX ix
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
	celsius = 36    	(degC)
	ek		(mV)
	ekk	= - 70	(mV)
	gkbar	= 5e-5	(mho/cm2)
	taumax	= 10	(ms)		: peak value of tau
	tau_m 	= 1 	(ms)
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

	m_inf = 1 / ( 1 + exptable(-(v+35)/10) )
}
UNITSON


FUNCTION exptable(x) { 
	TABLE  FROM -25 TO 25 WITH 10000

	if ((x > -25) && (x < 25)) {
		exptable = exp(x)
	} else {
		exptable = 0.
	}
}
