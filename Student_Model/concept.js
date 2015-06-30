// Requires: Util/serialization.js, Util/zet.js
if (typeof window === "undefined") {
    var window = this;
}

Zet.declare('Concept', {
	superclass : Serialization.Serializable,
    defineBody : function(self){
		// Public Properties
		
		// Constructor
		self.construct = function construct(conceptId, name, description){
			self.inherited(construct);
			self._conceptId = conceptId;
            self._name = name;
            self._description = description;
		};

        self.eq = function(other){
            return (self.CLASS_ID === other.CLASS_ID &&
                self._conceptId === other._conceptId &&
                self._name === other._name &&
                self._description === other._description);
        };
        
        self.neq = function(other){
            return (!self.eq(other));
        };
		
		// Public Methods
		self.initializeFromToken = function initializeFromToken(token, context){
			self.inherited(initializeFromToken, [token, context]);
			self._conceptId = token.getitem('conceptId', true, null);
            self._name = token.getitem('name', true, null);
            self._description = token.getitem('description', true, null);
		};

		self.saveToToken = function saveToToken(){
            var token;
			token = self.inherited(saveToToken);
			token.setitem('conceptId', self._conceptId);
            token.setitem('name', self._name);
            token.setitem('description', self._description);
			return token;
		};
	}
});