from http_content_parser.api_parser import ApiModelParser


api_parser = ApiModelParser()


def test_curl_parser():
    curl_file = "tests/curl"
    api_info = api_parser.get_api_model_for_curl(curl_file=curl_file)
    print(api_info)
