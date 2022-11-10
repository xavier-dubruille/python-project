from Class.DB import DBAccess as DB


class Brand(DB):
    def __init__(self):
        self.idBrand = None
        self.nameBrand = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Brand"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idDeal"

    @staticmethod
    def GetIdFromName(cls, name):
        cursor = DB.DBCursor()[0]
        try:
            cursor.execute(f"SELECT idBrand FROM Brand WHERE nameBrand = {name}")
            return cursor.fetchone()
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
