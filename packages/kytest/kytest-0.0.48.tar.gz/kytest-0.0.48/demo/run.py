import kytest


if __name__ == '__main__':
    # 主程序入口

    # android
    kytest.main(
        project='平台',
        path="tests/test_adr.py",
        serial=["UJK0220521066836", "30301cb9"],
        package="com.qizhidao.clientapp",
        strategy="split_parallel"
    )

    # api
    kytest.main(
        path="tests/test_api.py",
        project='平台',
        api_host='https://app-test.qizhidao.com'
    )

    # web
    kytest.main(
        project='平台',
        path="tests/test_web.py",
        web_host="https://www-test.qizhidao.com/",
    )
