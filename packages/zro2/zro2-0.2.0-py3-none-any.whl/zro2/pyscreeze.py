import time
from PIL import ImageGrab
import pyscreeze
import screeninfo
import typing

"""
provides easy import
"""
from pyscreeze import (  # noqa: E402
    USE_IMAGE_NOT_FOUND_EXCEPTION,
    ImageNotFoundException,
    center as center,
    locateAll as locateAll,
    locateAllOnScreen as locateAllOnScreen,
    locateCenterOnScreen as locateCenterOnScreen,
    locateOnScreen as locateOnScreen,
    locateOnWindow as locateOnWindow,
    pixel as pixel,
    pixelMatchesColor as pixelMatchesColor,
    screenshot as screenshot,
)

try:
    def locateAllPillow(needleImage, haystackImage, grayscale=None, limit=None, region=None, step=1, confidence=None):
        return pyscreeze._locateAll_pillow(needleImage, haystackImage, grayscale, limit, region, step, confidence) # type: ignore
except AttributeError:
    locateAllPillow = None # type: ignore

try:
    def locateAllOpenCV(needleImage, haystackImage, grayscale=None, limit=None, region=None, step=1, confidence=None):
        return pyscreeze._locateAll_opencv(needleImage, haystackImage, grayscale, limit, region, step, confidence) # type: ignore
except AttributeError:
    locateAllOpenCV = None # type: ignore


def locate(needleImage, haystackImage, _algo : typing.Literal["cv2", "pillow"] = "pillow",**kwargs):
    locallocateAll = locateAllOpenCV if _algo == "cv2" else locateAllPillow
    if locallocateAll is None:
        locallocateAll = locateAllPillow

    if locallocateAll is locateAllPillow:
        kwargs.pop("confidence", None)
    
    kwargs['limit'] = 1
    points = tuple(locallocateAll(needleImage, haystackImage, **kwargs))
    if len(points) > 0:
        return points[0]
    else:
        if USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise ImageNotFoundException('Could not locate the image.')
        else:
            return None

def waitTillImage(
    image: str,
    timeout: float = 10.0,
    interval: float = 1.0,
    confidence: float = 0.9,
    monitor: typing.Optional[screeninfo.Monitor] = None,
    region: typing.Optional[typing.Tuple[int, int, int, int]] = None
):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return None  # Timeout reached

        if monitor:
            # Capture the specific monitor
            screen_img = ImageGrab.grab(bbox=(monitor.x, monitor.y, monitor.width + monitor.x, monitor.height + monitor.y), all_screens=True)
        else:
            # Capture the primary monitor
            screen_img = ImageGrab.grab()

        if region:
            # Apply the region cropping
            screen_img = screen_img.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))

        # Try to locate the image on the screenshot
        try:
            result = locate(image, screen_img, confidence=confidence)
            if result:
                # Adjust result coordinates to reflect their position on the entire virtual desktop
                adjusted_result = (result.left + monitor.x, result.top + monitor.y, result.width, result.height)  # type: ignore
                return adjusted_result
        except pyscreeze.ImageNotFoundException:
            result = None

        time.sleep(interval)  # Wait before next attempt


def boxcenter(box):
    if isinstance(box, tuple):
        return center(box)
    return pyscreeze.Point(box.left + box.width / 2, box.top + box.height / 2)


