import pytest
import liburing


def test_sockaddr_class():
    with pytest.raises(NotImplementedError):
        liburing.sockaddr(123)
    # TODO: ?
    # with pytest.raises(ValueError):
    #     liburing.sockaddr(123, b'hello world hello world')  # length over 14

    # AF_UNIX
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_UNIX, b'')
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_UNIX, b' '*109)
    assert liburing.sockaddr(liburing.AF_UNIX, b'./path')._test == {
        'sun_family': 1, 'sun_path': b'./path'}

    # AF_INET
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET)
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET, b'', 123)
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET, b'./path')
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET, b'bad. ad.dre.ss', 123)
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET, b'::1', 123)  # ipv6 in ipv4
    assert liburing.sockaddr(liburing.AF_INET, b'0.0.0.0', 123)._test == {
        'sin_family': 2, 'sin_port': 31488, 'sin_addr': {'s_addr': 0}}
    assert liburing.sockaddr(liburing.AF_INET, b'127.0.0.1', 80)._test == {
        'sin_family': 2, 'sin_port': 20480, 'sin_addr': {'s_addr': 16777343}}

    # AF_INET6
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET6)
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET6, b'', 123)
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET6, b'./path')
    with pytest.raises(ValueError):
        liburing.sockaddr(liburing.AF_INET6, b'123.123.123.123', 123, 234)  # IPv4 in IPv6
    assert liburing.sockaddr(liburing.AF_INET6, b'::', 123, 321)._test == {
        'sin6_family': 10, 'sin6_port': 31488, 'sin6_flowinfo': 0,
        'sin6_addr': {'s6_addr': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
        'sin6_scope_id': 321}
    assert liburing.sockaddr(liburing.AF_INET6, b'::1', 65535)._test == {
        'sin6_family': 10, 'sin6_port': 65535, 'sin6_flowinfo': 0,
        'sin6_addr': {'s6_addr': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]},
        'sin6_scope_id': 0}


# @pytest.mark.skip('TODO')
# def test_sockadr_un_connect(ring, cqe):
#     ts = liburing.timespec(3)
#     # addr = liburing.sockaddr_un(b'/tmp/.X11-unix/X0')
#     addr = liburing.sockaddr_un(b'/tmp/.ICE-unix/1814')

#     # socket
#     sqe = liburing.io_uring_get_sqe(ring)
#     liburing.io_uring_prep_socket(sqe, liburing.AF_UNIX, liburing.SOCK_DGRAM)
#     sqe.user_data = 1
#     assert liburing.io_uring_submit_and_wait_timeout(ring, cqe, 1, ts) == 1
#     fd = liburing.trap_error(cqe.res)
#     assert cqe.user_data == 1
#     liburing.io_uring_cqe_seen(ring, cqe)

#     # connect
#     sqe = liburing.io_uring_get_sqe(ring)
#     liburing.io_uring_prep_connect(sqe, fd, addr)
#     sqe.user_data = 2
#     assert liburing.io_uring_submit_and_wait_timeout(ring, cqe, 1, ts) == 1
#     assert cqe.res == 0
#     assert cqe.user_data == 2
#     liburing.io_uring_cqe_seen(ring, cqe)

#     # shutdown & close
#     # sqe = liburing.io_uring_get_sqe(ring)
#     # liburing.io_uring_prep_shutdown(sqe, fd, liburing.SHUT_RDWR)
#     # sqe.flags = liburing.IOSQE_IO_LINK
#     # sqe.user_data = 3

#     sqe = liburing.io_uring_get_sqe(ring)
#     liburing.io_uring_prep_close(sqe, fd)
#     sqe.user_data = 3

#     assert liburing.io_uring_submit_and_wait_timeout(ring, cqe, 1, ts) == 1

#     # for i in range(2):
#     #     print('i:', i)
#     assert cqe.res == 0
#     assert cqe.user_data == 3
#     liburing.io_uring_cqe_seen(ring, cqe)

#     assert liburing.io_uring_submit_and_wait_timeout(ring, cqe, 1, ts) == 1
#     assert cqe.res == 0
#     assert cqe.user_data == 3
#     liburing.io_uring_cqe_seen(ring, cqe)
