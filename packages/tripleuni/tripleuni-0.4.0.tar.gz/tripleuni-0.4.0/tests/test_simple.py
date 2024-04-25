# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package



from tripleuni import TripleClient





if __name__ == '__main__':
    client = TripleClient("token")
    client.followPost(1)
