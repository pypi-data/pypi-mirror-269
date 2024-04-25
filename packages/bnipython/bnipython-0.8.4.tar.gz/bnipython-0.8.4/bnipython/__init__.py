from bnipython.lib.bniClient import BNIClient
from bnipython.lib.api.oneGatePayment import OneGatePayment
from bnipython.lib.api.snapBI import SnapBI
from bnipython.lib.api.rdn import RDN
from bnipython.lib.api.rdl import RDL
from bnipython.lib.api.rdf import RDF
from bnipython.lib.api.bniMove import BNIMove

import sys
sys.modules['BNIClient'] = BNIClient
sys.modules['OneGatePayment'] = OneGatePayment
sys.modules['SnapBI'] = SnapBI
sys.modules['RDN'] = RDN
sys.modules['RDF'] = RDF
sys.modules['RDL'] = RDL
sys.modules['BNIMove'] = BNIMove