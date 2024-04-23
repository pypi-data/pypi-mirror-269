import signal

should_stop = False


def pytest_addoption(parser):
    parser.addoption(
        "--continuous", action="store_true", default=False,
        help="Run tests continuously until failure or interrupted."
    )


def handle_stop_signal(signum, frame):
    global should_stop
    should_stop = True
    print("\nReceived stop signal, finishing after this test run...")


def pytest_sessionstart(session):
    if session.config.getoption("--continuous"):
        signal.signal(signal.SIGINT, handle_stop_signal)
        print("Running tests continuously. Press CTRL+C to stop...")


def pytest_runtestloop(session):
    if session.config.getoption("--continuous"):
        i = 0
        while not should_stop:
            for item in session.items:
                nextitem = session.items[(i + 1) % len(session.items)] if (i + 1) < len(session.items) else None
                session.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
                i += 1
                if session.testsfailed or should_stop:
                    return True
