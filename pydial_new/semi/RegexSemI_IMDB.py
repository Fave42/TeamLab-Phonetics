###############################################################################
# PyDial: Multi-domain Statistical Spoken Dialogue System Software
###############################################################################
#
# Copyright 2015 - 2017
# Cambridge University Engineering Department Dialogue Systems Group
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

"""
RegexSemI_CamRestaurants.py - regular expression based CamRestaurants SemI decoder
===============================================================


HELPFUL: http://regexr.com

"""

'''
    Modifications History
    ===============================
    Date        Author  Description
    ===============================
    Jul 21 2016 lmr46   Refactoring, creating abstract class SemI
'''

import RegexSemI
import re,os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
from utils import ContextLogger
logger = ContextLogger.getLogger('')


class RegexSemI_IMDB(RegexSemI.RegexSemI):
    """
    """
    def __init__(self, repoIn=None):
        RegexSemI.RegexSemI.__init__(self)  
        self.domainTag = "IMDB"  
        self.create_domain_dependent_regex()


    def create_domain_dependent_regex(self):
        self._domain_init(dstring=self.domainTag)
            
        # DOMAIN DEPENDENT SEMANTICS:
        self.slot_vocab= dict.fromkeys(self.USER_REQUESTABLE,'')
        self.slot_vocab["name"] = "(actor|actress|producer|composer|director|sound|music)"
        self.slot_vocab["birthyear"] = "(born|birth)"
        self.slot_vocab["deathyear"] = "(died|death)"
        self.slot_vocab["professions"] = "(profession|work|role)" 
        self.slot_vocab["movieinfo"] = "(movie|info|information|film|picture|series|documentary)"

        # Generate regular expressions for requests:
        self._set_request_regex()
            
        # FIXME:  many value have synonyms -- deal with this here:
        self._set_value_synonyms() 
        self._set_inform_regex()



    def _set_request_regex(self):
        """
        """
        self.request_regex = dict.fromkeys(self.USER_REQUESTABLE)
        for slot in self.request_regex.keys():
            self.request_regex[slot] = self.rREQUEST+"\ "+self.slot_vocab[slot]
            self.request_regex[slot] += "|(?<!"+self.DONTCAREWHAT+")(?<!want\ )"+self.IT+"\ "+self.slot_vocab[slot]
            self.request_regex[slot] += "|(?<!"+self.DONTCARE+")"+self.WHAT+"\ "+self.slot_vocab[slot]

        self.request_regex["name"] += "|(actor)|(actress)|(producer)|(composer)|(director)|(sound)|(music)"
        self.request_regex["birthyear"] += "|(born)|(birth)"
        self.request_regex["deathyear"] += "|(died)|(death)"
        self.request_regex["professions"] += "|(profession)|(work)|(role)"
        self.request_regex["movieinfo"] += "|(movie)|(info)|(information)|(film)"

    def _set_inform_regex(self):
        self.inform_regex = dict.fromkeys(self.USER_INFORMABLE)

        for slot in self.inform_regex.keys():
            self.inform_regex[slot] = {}

            for value in self.slot_values[slot].keys():
                self.inform_regex[slot][value] = self.rINFORM+"\ " + self.slot_values[slot][value]
                if slot == "name":
                    self.inform_regex[slot][value] += "|(named|called|by the name|)" + self.slot_values[slot][value]
                if slot == "birthyear":
                    self.inform_regex[slot][value] += "|(was born in|born|birth|)" + self.slot_values[slot][value]
                if slot == "deathyear":
                    self.inform_regex[slot][value] += "|(died in|died|dead|)" + self.slot_values[slot][value]
                if slot == "professions":
                    self.inform_regex[slot][value] += "|(worked as|role|starred|profession|job|work|)" + self.slot_values[slot][value]
                if slot == "movieinfo":
                    self.inform_regex[slot][value] += "|(starred in|known|movies|films|info|series|)" + self.slot_values[slot][value]


    def _generic_request(self,obs,slot):
        """
        """
        if self._check(re.search(self.request_regex[slot],obs, re.I)):
            self.semanticActs.append('request('+slot+')')

    def _generic_inform(self,obs,slot):
        """
        """
        
        
        
        DETECTED_SLOT_INTENT = False
        for value in self.inform_regex[slot]:
            if self._check(re.search(self.inform_regex[slot][value],obs, re.I)):
                #FIXME:  Think easier to parse here for "dont want" and "dont care" - else we're playing "WACK A MOLE!"
                ADD_SLOTeqVALUE = True
#                 # Deal with -- DONTWANT --:
#                 if self._check(re.search(self.rINFORM_DONTWANT+"\ "+self.slot_values[slot][value], obs, re.I)): 
#                     self.semanticActs.append('inform('+slot+'!='+value+')')  #TODO - is this valid?
#                     ADD_SLOTeqVALUE = False
#                 # Deal with -- DONTCARE --:
#                 if self._check(re.search(self.rINFORM_DONTCARE+"\ "+slot, obs, re.I)) and not DETECTED_SLOT_INTENT:
#                     self.semanticActs.append('inform('+slot+'=dontcare)')
#                     ADD_SLOTeqVALUE = False
#                     DETECTED_SLOT_INTENT = True
                # Deal with -- REQUESTS --: (may not be required...)
                #TODO? - maybe just filter at end, so that inform(X) and request(X) can not both be there?
                if ADD_SLOTeqVALUE and not DETECTED_SLOT_INTENT:
                    self.semanticActs.append('inform('+slot+'='+value+')')

    def _decode_request(self, obs):
        """
        """
        # if a slot needs its own code, then add it to this list and write code to deal with it differently
        DO_DIFFERENTLY= [] #FIXME 
        for slot in self.USER_REQUESTABLE:
            if slot not in DO_DIFFERENTLY:
                self._generic_request(obs,slot)
        # Domain independent requests:
        self._domain_independent_requests(obs)

        
    def _decode_inform(self, obs):
        """
        """
        # if a slot needs its own code, then add it to this list and write code to deal with it differently
        DO_DIFFERENTLY= [] #FIXME 
        for slot in self.USER_INFORMABLE:
            if slot not in DO_DIFFERENTLY:
                self._generic_inform(obs,slot)
        # Check other statements that use context
        self._contextual_inform(obs)

    def _decode_type(self,obs):
        """
        """
        # This is pretty ordinary - will just keyword spot for now since type really serves no point at all in our system
        if self._check(re.search(self.inform_type_regex,obs, re.I)):
            self.semanticActs.append('inform(type='+self.domains_type+')')


    def _decode_confirm(self, obs):
        """
        """
        #TODO?
        pass


    def _set_value_synonyms(self):
        # TYPE:
        self.inform_type_regex = r"(actor|actress|movie)"

#END OF FILE
