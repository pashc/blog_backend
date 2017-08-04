from flask_restplus import reqparse

request_parser = reqparse.RequestParser()
request_parser.add_argument('page', type=int, required=False, default=1, help='page number')
request_parser.add_argument('is_current', type=bool, required=False, default=True, help='is current page')
request_parser.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                            default=10, help='Results per page {error_msg}')
