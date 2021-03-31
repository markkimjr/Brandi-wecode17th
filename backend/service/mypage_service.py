from model.mypage_dao   import MyPageDao
from flask              import jsonify, json
from errors             import *

class MyPageService:

    def mypage_qna(self, connection, user_id, page_condition, answer):
        mypage_dao = MyPageDao()
        mypage_qna = mypage_dao.mypyage_qna_dao(connection, user_id, page_condition, answer)
        #totalCount 수 반환
        mypage_count = mypage_dao.mypage_qna_count(connection, user_id, answer)[0]
        total_count = mypage_count['COUNT(*)']

        result = []
        for row in mypage_qna:
            question = {
                'id'            : row['id'],
                'username'      : row['username'],
                'contents'      : row['contents'],
                'category'      : row['category'],
                'created_at'    : row['created_at']
            }
            # 답변이 있는경우 answer에 담아줌
            if row['answer_id']:
                question['answer'] = {
                    'id'            : row['answer_id'],
                    'replier'       : row['answer_replier'],
                    'content'       : row['answer_content'],
                    'created_at'    : row['answer_time'],
                    'parent_id'     : row['answer_parent']
                }
            result.append(question)
        return {"data" : result, "totalCount" : total_count}

    def mypage_order(self, connection, user_id, page_condition):
        mypage_dao = MyPageDao()
        #totalCount수 반환
        order_count = mypage_dao.mypage_order_count(connection, user_id)[0]
        total_count = order_count['COUNT(*)']

        # 로그인 유저의 주문 목록 반환
        order_header = mypage_dao.mypage_order_header_dao(connection, user_id, page_condition)
        order_id = [o['id'] for o in order_header]
        
        # 해당되는 주문목록에 속하는 구매 목록 반환
        order_cart = mypage_dao.mypage_order_cart_dao(connection, user_id, page_condition, order_id)
        order_list = [{
            "orderId" : order_head['id'],
            "ordernum" : order_head['order_number'],
            "ordertime" : order_head['created_at'],
            'product': []
        } for order_head in order_header]

        for cart in order_cart:
            order_num = cart['orderNumber']
            brand = cart['brand']
            order = list(filter(lambda d: d['ordernum'] == order_num,  order_list))[0]
            option_brand = list(filter(lambda d: d['brand'] == brand,  order['product']))
            if not option_brand:
                option_brand = {'brand': brand, 'option':[]}
                order['product'].append(option_brand)
            else:
                option_brand = option_brand[0]
            option_brand['option'].append(cart)

        return {"data" : order_list, "totalCount" : total_count}

    # 상세 주문내역 (로그인 유저의 주문번호 1건에 대한 내용)
    def mypage_order_detail(self, connection, user_id, order_id):
        mypage_dao = MyPageDao()
        mypage_order_detail= mypage_dao.mypage_order_detail_header_dao(connection, user_id, order_id)
        products_list = mypage_order_detail['detailProducts']
        order = mypage_order_detail['detailHeader']
        brand_name = []

        # 중복 없이 한건의 주문내역에 포함되는 판매 브랜드 이름 배열
        for one_brand in products_list:
            brand_name.append(one_brand['brand'])
        brand_name_one = list(set(brand_name))

        order_dict = {
            "orderId" : order['id'],
            "orderNum" : order['order_number'],
            "orderTime" : order['created_at'],
            "orderName" : order['username'], #username말고 order_name으로 바뀔것
            "discountPrice" : order['total_price'],
            "product" : 
                [{
                    "brand" : one
                } for one in brand_name_one]
        }
        # 같은 브랜드의 상품을 배열 안에 묶어주는 로직
        for one_brand_name in order_dict['product']:
            brand = one_brand_name['brand']
            product_options = list(filter(lambda x:x['brand'] == brand, products_list))
            one_brand_name['option'] = product_options
 
        return {"data" : order_dict}
