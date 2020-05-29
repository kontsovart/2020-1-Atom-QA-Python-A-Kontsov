import time
import os


def wait(method, error=Exception, timeout=20, interval=1, check=False, **kwargs):
    st = time.time()
    while time.time() - st < timeout:
        try:
            result = method(**kwargs)
            if check:
                if result:
                    return result
            else:
                return result
        except error:
            pass
        time.sleep(interval)
    raise TimeoutError("Timeout was reached during operation '%s'. See details in debug log" % method.__name__)


def passage(file_name, folder):
    for element in os.scandir(folder):
        if element.is_file():
            if element.name == file_name:
                yield folder + '/' + file_name
        else:
            yield from passage(file_name, element.path)
