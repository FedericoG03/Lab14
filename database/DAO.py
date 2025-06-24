from database.DB_connect import DBConnect
from model.Node import Order


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct store_id 
                    from stores s 
                     """

        cursor.execute(query)

        for row in cursor:
            result.append((row['store_id']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                    from orders o 
                    where store_id = %s
                         """

        cursor.execute(query,(store,))

        for row in cursor:
            result.append(Order(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(numGiorni,store,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct o1.order_id as ord1,o2.order_id as ord2, count(oi1.quantity+oi2.quantity) as peso
                    from orders o1, orders o2, order_items oi1, order_items oi2 
                    where o1.store_id = o2.store_id 
                    and o2.store_id = %s
                    and o1.order_id > o2.order_id 
                    and oi1.order_id = o1.order_id
                    and oi2.order_id = o2.order_id 
                    and datediff(o1.order_date,o2.order_date) < %s
                    and abs(datediff(o1.order_date,o2.order_date)) > 0
                    group by o1.order_id ,o2.order_id
                             """

        cursor.execute(query, (store, numGiorni))

        for row in cursor:
            result.append((idMap[row['ord1']],idMap[row['ord2']],row['peso']))
        cursor.close()
        conn.close()
        return result


