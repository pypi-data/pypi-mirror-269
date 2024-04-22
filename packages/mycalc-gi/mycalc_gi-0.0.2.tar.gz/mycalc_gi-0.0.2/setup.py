from setuptools import setup, find_packages


#https://pypi.org/help/#invalid-auth
#pypi-AgEIcHlwaS5vcmcCJDRlYzZhOWU3LTZhOWQtNDk2NS05NTY0LTU4OTNkZTA0ODE5ZQACKlszLCIxNGIwMDY1OS1lYzIzLTQ2ZmEtOTI1OS01MjMwNDFmMWFlYjkiXQAABiB6lwDDvR4DrQqzN3JdL7qZN9X-OnqAgDbkAwXa7jWPVw
#api 토큰
#ppt의 방식으로 업대이트를 해보자
#뭘 추가 해야 하는가...
#확통 껄 계량하자

setup(
    name='mycalc_gi',
    version='0.0.2',
    description='nice calculator',
    author='gitaebak',
    url = 'https://github.com/GitaeBak/unv_oss',
    download_url = "https://github.com/GitaeBak/unv_oss",
    install_requires=["pandas","numpy","matplotlib"],
    package=["mycalc"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)