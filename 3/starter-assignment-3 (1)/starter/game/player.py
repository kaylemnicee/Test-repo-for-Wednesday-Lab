

class Player:
    
    def __init__(self, id : int, resource : int =0):
        self._ID = id
        self._resource = resource
    
     #Returns the player ID
    def getID(self) -> int:
        return self._ID

    #Returns the amount of resources owned by the player
    def getResources(self) -> int:
        return self._resource

    #Sets the amount of resources owned by the player
    def setResources(self, a_resources:int) -> None:
        self._resource = a_resources     



    def  toString(self)->str:
        return "player " + str(self._ID) + "(" + str(self._resource) + ")";
    

     
    def  clone(self):
        pass

    '''
         * Writes a XML representation of the player
         * @param w
        public void toxml(XMLWriter w) {
            w.tagWithAttributes(this.getClass().getName(), "ID=\"" + ID + "\" resources=\"" + resources + "\"");
            w.tag("/" + this.getClass().getName());
        }
        */

        /**
         * Writes a JSON representation of the player
         * @param w
         * @throws Exception
     
        public void toJSON(Writer w) throws Exception {
            w.write("{\"ID\":" + ID + ", \"resources\":" + resources + "}");
        }
     '''
     

    #Constructs a player from a XML player element
    @staticmethod
    def fromXML(xml_node ):
       
        id_p = int(xml_node.attrib["ID"])
        resources = int(xml_node.attrib["resources"])
        player = Player(id_p,resources) 
        return player

    '''
         * Constructs a Player from a JSON object
         * @param o
         * @return
     
        public static Player fromJSON(JsonObject o) {
            Player p = new Player(o.getInt("ID", -1),
                o.getInt("resources", 0));
            return p;
        }
    '''