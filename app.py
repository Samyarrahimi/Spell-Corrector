from flask import Flask, request, make_response, render_template, jsonify
from flask_restful import Resource, Api
from lib.Query import get, validation_test, empty_filter, make_it_ok

app = Flask(__name__, template_folder='templates')
api = Api(app)


# handle get request
class ReqHandler(Resource):
    def get(self):
        args = request.args
        query = args['q']
        query = query.lstrip(" ")
        query = query.rstrip(" ")
        is_valid = validation_test(query)
        if is_valid:
            query = make_it_ok(query)
            ans = get(query)
            res = empty_filter(ans)

            if len(res) < 2:
                index = render_template("index.html", qu=query,
                                        p1=(res[0] if len(res) > 0 else ""),
                                        p2="", p3="", p4="", p5="", p6="", p7="", p8="",
                                        p9="", p10="")
            elif res[0] == res[1]:
                index = render_template("index.html", qu=query,
                                        p1=(res[0] if len(res) > 0 else ""),
                                        p2="", p3="", p4="", p5="", p6="", p7="", p8="",
                                        p9="", p10="")
            else:
                index = render_template("index.html", qu=query,
                                        p1=(res[0] if len(res) > 0 else ""),
                                        p2=(res[1] if len(res) > 1 else ""),
                                        p3=(res[2] if len(res) > 2 else ""),
                                        p4=(res[3] if len(res) > 3 else ""),
                                        p5=(res[4] if len(res) > 4 else ""),
                                        p6=(res[5] if len(res) > 5 else ""),
                                        p7=(res[6] if len(res) > 6 else ""),
                                        p8=(res[7] if len(res) > 7 else ""),
                                        p9=(res[8] if len(res) > 8 else ""),
                                        p10=(res[9] if len(res) > 9 else ""))
            return make_response(index)
        else:
            index = render_template("index.html",
                                    p1="Your query is not acceptable", p2="Please enter persian characters"
                                    , p3="", p4="", p5="", p6="", p7="", p8="", p9="", p10=""), 406
            return make_response(index)


# return index.html
class IndexHandler(Resource):
    def get(self):
        index = render_template("index.html",
                                p1="", p2="", p3="", p4="", p5="", p6="", p7="", p8="", p9="", p10="")
        return make_response(index)


api.add_resource(ReqHandler, '/search')
api.add_resource(IndexHandler, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
